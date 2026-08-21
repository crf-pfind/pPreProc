"""Command-line inspection utility for PFB/PFC v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .reader import PFBReader


def _record_summary(record) -> dict[str, object]:
    return {
        "index": record.index,
        "scan_number": record.scan_number,
        "peak_count": record.peak_count,
        "record_start": record.start_pos,
        "record_end": record.end_pos,
        "property_text": record.property_text,
        "metadata": record.metadata,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ppreproc-pfb",
        description="Inspect and validate pPreProc PFB/PFC v1 files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    info = subparsers.add_parser("info", help="show file-level information")
    info.add_argument("pfb", type=Path)

    validate = subparsers.add_parser("validate", help="validate a PFB/PFC pair")
    validate.add_argument("pfb", type=Path)
    validate.add_argument("--full", action="store_true")

    spectrum = subparsers.add_parser("spectrum", help="retrieve one spectrum")
    spectrum.add_argument("pfb", type=Path)
    selection = spectrum.add_mutually_exclusive_group(required=True)
    selection.add_argument("--index", type=int)
    selection.add_argument("--scan")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    with PFBReader(args.pfb) as reader:
        if args.command == "info":
            output = {
                "pfb": str(reader.pfb_path),
                "pfc": str(reader.pfc_path),
                "file_size": reader.file_size,
                "spectrum_count": len(reader),
                "index_address": reader.index_address,
                "pfc_columns": reader.pfc_fieldnames,
            }
        elif args.command == "validate":
            output = reader.validate(full=args.full)
        else:
            record = (
                reader.get_spectrum(args.index, with_arrays=False)
                if args.index is not None
                else reader.get_spectrum_by_scan(args.scan, with_arrays=False)
            )
            output = _record_summary(record)
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0
