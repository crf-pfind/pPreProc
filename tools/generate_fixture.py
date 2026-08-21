"""Generate the tiny synthetic PFB/PFC pair used by interface tests."""

from __future__ import annotations

import csv
import struct
from pathlib import Path


HEADER = struct.Struct("<iiiQi")
UINT32 = struct.Struct("<I")
UINT64 = struct.Struct("<Q")
DOUBLE = struct.Struct("<d")


RECORDS = [
    ("MS1 synthetic", [499.9, 500.2, 501.0], [10.0, 120.0, 20.0]),
    ("MS2 synthetic", [100.1, 200.2], [200.0, 50.0]),
    ("MS1 synthetic", [500.2, 700.0], [80.0, 5.0]),
]

FIELDS = [
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
]

ROWS = [
    {"ScanNo": "101", "RetTime": "10.0", "SpectrumType": "MS1"},
    {
        "ScanNo": "102",
        "PrecursorScan": "101",
        "RetTime": "10.2",
        "SpectrumType": "MS2",
        "activationType": "HCD",
        "monoIsotopicMz": "500.2",
    },
    {"ScanNo": "103", "RetTime": "11.0", "SpectrumType": "MS1"},
]


def generate(destination: Path) -> tuple[Path, Path]:
    destination.mkdir(parents=True, exist_ok=True)
    pfb = destination / "minimal.pfb"
    pfc = destination / "minimal.pfc"
    with pfb.open("wb+") as handle:
        handle.write(b"\0" * HEADER.size)
        offsets = []
        for text, mz_values, intensity_values in RECORDS:
            offsets.append(handle.tell())
            encoded = text.encode("utf-8")
            handle.write(UINT32.pack(len(encoded)))
            handle.write(encoded)
            handle.write(UINT32.pack(len(mz_values)))
            for value in mz_values:
                handle.write(DOUBLE.pack(value))
            for value in intensity_values:
                handle.write(DOUBLE.pack(value))
        index_address = handle.tell()
        for offset in offsets:
            handle.write(UINT64.pack(offset))
        handle.seek(0)
        handle.write(HEADER.pack(0, 0, 0, index_address, len(RECORDS)))

    with pfc.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDS,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for index, (source, record) in enumerate(zip(ROWS, RECORDS)):
            row = {field: "" for field in FIELDS}
            row.update(source)
            row["InstrumentType"] = "Synthetic"
            row["NumberofPeaks"] = str(len(record[1]))
            row["StartPos"] = str(offsets[index])
            row["EndPos"] = str(
                offsets[index + 1] if index + 1 < len(offsets) else index_address
            )
            writer.writerow(row)
    return pfb, pfc


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    generated = generate(root / "tests" / "fixtures")
    print("\n".join(str(path) for path in generated))
