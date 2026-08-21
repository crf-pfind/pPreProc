"""Print a compact summary for one scan in an indexed PFB/PFC pair."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ppreproc_pfb import PFBReader


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pfb", type=Path)
    parser.add_argument("scan")
    args = parser.parse_args()

    with PFBReader(args.pfb) as reader:
        record = reader.get_spectrum_by_scan(args.scan)
        result = {
            "scan_number": record.scan_number,
            "peak_count": record.peak_count,
            "retention_time": record.metadata.get("RetTime"),
            "first_mz": record.mz[0] if record.mz else None,
        }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
