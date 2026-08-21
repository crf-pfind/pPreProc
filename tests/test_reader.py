from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ppreproc_pfb import PFBFormatError, PFBReader  # noqa: E402
from tools.generate_fixture import generate  # noqa: E402


class ReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pfb, cls.pfc = generate(ROOT / "tests" / "fixtures")

    def test_header_and_direct_record_access(self) -> None:
        with PFBReader(self.pfb) as reader:
            self.assertEqual(len(reader), 3)
            self.assertEqual(reader.offsets[0], 24)
            record = reader.get_spectrum(1)
            self.assertEqual(record.scan_number, "102")
            self.assertEqual(record.peak_count, 2)
            self.assertEqual(list(record.mz), [100.1, 200.2])
            self.assertEqual(list(record.intensity), [200.0, 50.0])

    def test_scan_and_parent_access(self) -> None:
        with PFBReader(self.pfb) as reader:
            ms2 = reader.get_spectrum_by_scan(102)
            parent = reader.get_parent_ms1(ms2)
            self.assertEqual(parent.scan_number, "101")
            self.assertEqual(parent.metadata["SpectrumType"], "MS1")

    def test_xic_and_full_validation(self) -> None:
        with PFBReader(self.pfb) as reader:
            self.assertEqual(
                reader.extract_xic(500.2, 10, 9.5, 11.5),
                [(10.0, 120.0), (11.0, 80.0)],
            )
            report = reader.validate(full=True)
            self.assertEqual(report["decoded_spectra"], 3)
            self.assertEqual(report["decoded_peaks"], 7)
            self.assertEqual(report["validated_parent_links"], 1)

    def test_missing_pfc_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "orphan.pfb"
            target.write_bytes(self.pfb.read_bytes())
            with self.assertRaises(PFBFormatError):
                PFBReader(target)
            with PFBReader(target, require_pfc=False) as reader:
                self.assertEqual(len(reader), 3)

    def test_truncated_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "truncated.pfb"
            target.write_bytes(self.pfb.read_bytes()[:-1])
            with self.assertRaises(PFBFormatError):
                PFBReader(target, require_pfc=False)

    def test_pfc_peak_count_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target_pfb = Path(temporary) / "mismatch.pfb"
            target_pfc = Path(temporary) / "mismatch.pfc"
            target_pfb.write_bytes(self.pfb.read_bytes())
            lines = self.pfc.read_text(encoding="utf-8").splitlines()
            header = lines[0].split("\t")
            values = lines[1].split("\t")
            values[header.index("NumberofPeaks")] = "999"
            lines[1] = "\t".join(values)
            target_pfc.write_text("\n".join(lines) + "\n", encoding="utf-8")
            with PFBReader(target_pfb) as reader:
                with self.assertRaises(PFBFormatError):
                    reader.validate(full=True)

    def test_cli_info(self) -> None:
        environment = dict(__import__("os").environ)
        environment["PYTHONPATH"] = str(SRC)
        completed = subprocess.run(
            [sys.executable, "-m", "ppreproc_pfb", "info", str(self.pfb)],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        self.assertEqual(json.loads(completed.stdout)["spectrum_count"], 3)


if __name__ == "__main__":
    unittest.main()
