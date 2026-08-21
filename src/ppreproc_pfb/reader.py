"""Reader utilities for the indexed pPreProc PFB/PFC v1 pair.

PFB v1 is a little-endian binary format.  Its 24-byte header is followed by
variable-length spectrum records and a footer containing one uint64 record
offset per spectrum.  PFC is the tab-delimited metadata companion.  The
footer allows a record to be retrieved without scanning preceding records.
"""

from __future__ import annotations

import bisect
import csv
import math
import mmap
import struct
import sys
from array import array
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


FORMAT_VERSION = 1
HEADER_SIZE = 24
HEADER = struct.Struct("<iiiQi")
UINT32 = struct.Struct("<I")
UINT64 = struct.Struct("<Q")
CORE_PFC_FIELDS = (
    "ScanNo",
    "PrecursorScan",
    "RetTime",
    "SpectrumType",
    "InstrumentType",
    "IonInjectionTime",
    "activationType",
    "activationCenter",
    "NCE",
    "monoIsotopicMz",
    "upperCharge",
    "lowerCharge",
    "activationWindow",
    "NumberofPeaks",
    "StartPos",
    "EndPos",
)


class PFBFormatError(RuntimeError):
    """Raised when a PFB/PFC pair violates the documented v1 contract."""


def _double_array(raw: bytes) -> array:
    values = array("d")
    values.frombytes(raw)
    if sys.byteorder != "little":
        values.byteswap()
    return values


@dataclass(frozen=True)
class PFBRecord:
    """One decoded spectrum and its companion metadata."""

    index: int
    start_pos: int
    end_pos: int
    property_text: str
    peak_count: int
    mz: array
    intensity: array
    metadata: dict[str, str]

    @property
    def scan_number(self) -> str | None:
        value = self.metadata.get("ScanNo", "").strip()
        return value or None


class PFBReader:
    """Open and randomly access a PFB/PFC v1 pair.

    Parameters
    ----------
    pfb_path:
        Path to the binary PFB file.
    pfc_path:
        Optional explicit PFC path.  By default, the companion with the same
        stem is used.
    require_pfc:
        Require the PFC companion.  Set to ``False`` only for low-level PFB
        inspection; scan and parent metadata operations then remain
        unavailable.
    """

    def __init__(
        self,
        pfb_path: str | Path,
        pfc_path: str | Path | None = None,
        *,
        require_pfc: bool = True,
    ) -> None:
        self.pfb_path = Path(pfb_path).resolve()
        self.pfc_path = (
            Path(pfc_path).resolve()
            if pfc_path is not None
            else self.pfb_path.with_suffix(".pfc")
        )
        self._handle = self.pfb_path.open("rb")
        try:
            self._map = mmap.mmap(self._handle.fileno(), 0, access=mmap.ACCESS_READ)
            self.file_size = len(self._map)
            (
                self.reserved_header,
                self.index_address,
                self.spectrum_count,
            ) = self._read_header()
            self.offsets = self._read_index()
            self.pfc_fieldnames, self.pfc_rows = self._read_pfc(require_pfc)
            self.scan_to_index = self._build_scan_index()
            self._validate_structure()
        except Exception:
            if hasattr(self, "_map"):
                self._map.close()
            self._handle.close()
            raise

    def close(self) -> None:
        self._map.close()
        self._handle.close()

    def __enter__(self) -> "PFBReader":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def _read_header(self) -> tuple[tuple[int, int, int], int, int]:
        if self.file_size < HEADER_SIZE:
            raise PFBFormatError("PFB is smaller than its 24-byte v1 header")
        reserved_one, reserved_two, reserved_three, index_address, count = (
            HEADER.unpack_from(self._map, 0)
        )
        if count < 0:
            raise PFBFormatError(f"negative spectrum count: {count}")
        return (
            (reserved_one, reserved_two, reserved_three),
            int(index_address),
            int(count),
        )

    def _read_index(self) -> list[int]:
        if not HEADER_SIZE <= self.index_address <= self.file_size:
            raise PFBFormatError(
                f"invalid index address {self.index_address} for "
                f"file size {self.file_size}; this is not an indexed "
                "PFB/PFC v1 file (it may be a legacy or corrupt PFB)"
            )
        expected_bytes = self.spectrum_count * UINT64.size
        actual_bytes = self.file_size - self.index_address
        if actual_bytes != expected_bytes:
            raise PFBFormatError(
                f"index-size mismatch: file tail={actual_bytes}, "
                f"expected={expected_bytes}"
            )
        return [
            UINT64.unpack_from(
                self._map,
                self.index_address + index * UINT64.size,
            )[0]
            for index in range(self.spectrum_count)
        ]

    def _read_pfc(
        self,
        require_pfc: bool,
    ) -> tuple[list[str], list[dict[str, str]]]:
        if not self.pfc_path.is_file():
            if require_pfc:
                raise PFBFormatError(f"missing companion PFC: {self.pfc_path}")
            return [], []
        with self.pfc_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if not reader.fieldnames:
                raise PFBFormatError("PFC has no header")
            missing = [
                field for field in CORE_PFC_FIELDS if field not in reader.fieldnames
            ]
            if missing:
                raise PFBFormatError(
                    "PFC is missing v1 columns: " + ", ".join(missing)
                )
            rows = list(reader)
        return list(reader.fieldnames), rows

    def _build_scan_index(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for index, row in enumerate(self.pfc_rows):
            scan = row.get("ScanNo", "").strip()
            if not scan:
                raise PFBFormatError(f"PFC row {index} has no ScanNo")
            if scan in result:
                raise PFBFormatError(f"duplicate PFC ScanNo: {scan}")
            result[scan] = index
        return result

    def _validate_structure(self) -> None:
        if self.pfc_rows and len(self.pfc_rows) != self.spectrum_count:
            raise PFBFormatError(
                f"PFC rows={len(self.pfc_rows)} but "
                f"PFB spectra={self.spectrum_count}"
            )
        if not self.spectrum_count:
            if self.index_address != HEADER_SIZE:
                raise PFBFormatError("empty PFB has a non-empty data region")
            return
        if self.offsets[0] != HEADER_SIZE:
            raise PFBFormatError(
                f"first record begins at {self.offsets[0]}, expected {HEADER_SIZE}"
            )
        if any(left >= right for left, right in zip(self.offsets, self.offsets[1:])):
            raise PFBFormatError("PFB record offsets are not strictly increasing")
        if self.offsets[-1] >= self.index_address:
            raise PFBFormatError("last record offset lies outside the data region")

    def _normalize_index(self, index: int) -> int:
        normalized = index + self.spectrum_count if index < 0 else index
        if not 0 <= normalized < self.spectrum_count:
            raise IndexError(index)
        return normalized

    def _record_bounds(self, index: int) -> tuple[int, int, int]:
        normalized = self._normalize_index(index)
        start = self.offsets[normalized]
        end = (
            self.offsets[normalized + 1]
            if normalized + 1 < self.spectrum_count
            else self.index_address
        )
        return normalized, start, end

    def get_spectrum(self, index: int, *, with_arrays: bool = True) -> PFBRecord:
        """Retrieve one spectrum directly through its footer offset."""

        normalized, start, end = self._record_bounds(index)
        cursor = start
        if cursor + UINT32.size > end:
            raise PFBFormatError(f"record {normalized} lacks a property length")
        property_size = UINT32.unpack_from(self._map, cursor)[0]
        cursor += UINT32.size
        property_end = cursor + property_size
        if property_end + UINT32.size > end:
            raise PFBFormatError(
                f"record {normalized} property string exceeds its boundary"
            )
        property_text = self._map[cursor:property_end].decode("utf-8").rstrip("\x00")
        cursor = property_end
        peak_count = UINT32.unpack_from(self._map, cursor)[0]
        cursor += UINT32.size
        array_bytes = peak_count * 8
        decoded_end = cursor + 2 * array_bytes
        if decoded_end != end:
            raise PFBFormatError(
                f"record {normalized} ends at {end}, decoded end is {decoded_end}"
            )
        if with_arrays:
            mz = _double_array(self._map[cursor : cursor + array_bytes])
            intensity = _double_array(
                self._map[cursor + array_bytes : decoded_end]
            )
        else:
            mz = array("d")
            intensity = array("d")
        metadata = self.pfc_rows[normalized] if self.pfc_rows else {}
        return PFBRecord(
            index=normalized,
            start_pos=start,
            end_pos=end,
            property_text=property_text,
            peak_count=peak_count,
            mz=mz,
            intensity=intensity,
            metadata=metadata,
        )

    def get_spectrum_by_scan(
        self,
        scan_number: str | int,
        *,
        with_arrays: bool = True,
    ) -> PFBRecord:
        """Retrieve a spectrum using the PFC ``ScanNo`` field."""

        scan = str(scan_number)
        try:
            index = self.scan_to_index[scan]
        except KeyError as error:
            raise KeyError(f"unknown PFC ScanNo: {scan}") from error
        return self.get_spectrum(index, with_arrays=with_arrays)

    def get_parent_ms1(
        self,
        spectrum: int | PFBRecord,
        *,
        with_arrays: bool = True,
    ) -> PFBRecord:
        """Follow PFC parent links until the corresponding MS1 is reached."""

        if not self.pfc_rows:
            raise PFBFormatError("parent lookup requires the companion PFC")
        record = (
            self.get_spectrum(spectrum, with_arrays=False)
            if isinstance(spectrum, int)
            else spectrum
        )
        parent_scan = record.metadata.get("PrecursorScan", "").strip()
        if not parent_scan:
            raise PFBFormatError(f"spectrum {record.index} declares no parent scan")
        visited = {record.metadata.get("ScanNo", "")}
        while True:
            if parent_scan in visited:
                raise PFBFormatError("cycle detected while resolving parent MS1")
            visited.add(parent_scan)
            parent = self.get_spectrum_by_scan(parent_scan, with_arrays=False)
            if parent.metadata.get("SpectrumType", "").upper() == "MS1":
                return (
                    self.get_spectrum(parent.index, with_arrays=True)
                    if with_arrays
                    else parent
                )
            parent_scan = parent.metadata.get("PrecursorScan", "").strip()
            if not parent_scan:
                raise PFBFormatError(
                    f"scan {parent.scan_number} is not MS1 and has no parent"
                )

    def iter_spectra(self, *, with_arrays: bool = True) -> Iterator[PFBRecord]:
        for index in range(self.spectrum_count):
            yield self.get_spectrum(index, with_arrays=with_arrays)

    def __iter__(self) -> Iterator[PFBRecord]:
        return self.iter_spectra()

    def __len__(self) -> int:
        return self.spectrum_count

    def validate(self, *, full: bool = False) -> dict[str, int | bool]:
        """Validate the index and optionally decode all records and parent links."""

        decoded_spectra = 0
        decoded_peaks = 0
        parent_links = 0
        if full:
            for record in self.iter_spectra():
                row = record.metadata
                try:
                    declared_peaks = int(row["NumberofPeaks"])
                    declared_start = int(row["StartPos"])
                    declared_end = int(row["EndPos"])
                    float(row["RetTime"])
                except (KeyError, TypeError, ValueError) as error:
                    raise PFBFormatError(
                        f"record {record.index} has invalid numeric PFC metadata"
                    ) from error
                if declared_peaks != record.peak_count:
                    raise PFBFormatError(
                        f"record {record.index} peak-count mismatch: "
                        f"PFC={declared_peaks}, PFB={record.peak_count}"
                    )
                if (declared_start, declared_end) != (
                    record.start_pos,
                    record.end_pos,
                ):
                    raise PFBFormatError(
                        f"record {record.index} PFC/PFB byte-boundary mismatch"
                    )
                decoded_spectra += 1
                decoded_peaks += record.peak_count
                if record.metadata.get("PrecursorScan", "").strip():
                    self.get_parent_ms1(record, with_arrays=False)
                    parent_links += 1
        return {
            "format_version": FORMAT_VERSION,
            "structure_valid": True,
            "full_decode": full,
            "spectrum_count": self.spectrum_count,
            "decoded_spectra": decoded_spectra,
            "decoded_peaks": decoded_peaks,
            "validated_parent_links": parent_links,
            "pfc_present": bool(self.pfc_rows),
        }

    def extract_xic(
        self,
        target_mz: float,
        ppm: float,
        rt_start: float,
        rt_end: float,
        *,
        faims_cv: float | None = None,
    ) -> list[tuple[float, float]]:
        """Extract a simple MS1 chromatogram from the paired representation."""

        if not self.pfc_rows:
            raise PFBFormatError("XIC extraction requires the companion PFC")
        tolerance = target_mz * ppm * 1e-6
        lower, upper = target_mz - tolerance, target_mz + tolerance
        points: list[tuple[float, float]] = []
        for index, row in enumerate(self.pfc_rows):
            if row.get("SpectrumType", "").upper() != "MS1":
                continue
            rt = float(row["RetTime"])
            if not rt_start <= rt <= rt_end:
                continue
            if faims_cv is not None:
                value = row.get("FAIMS_Voltage", "").strip()
                if not value or not math.isclose(float(value), faims_cv):
                    continue
            spectrum = self.get_spectrum(index)
            left = bisect.bisect_left(spectrum.mz, lower)
            right = bisect.bisect_right(spectrum.mz, upper)
            points.append((rt, float(sum(spectrum.intensity[left:right]))))
        return points
