"""Perform repository and optional pFind-runtime release checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-bin", type=Path)
    parser.add_argument(
        "--artifact",
        choices=("development", "source", "binary"),
        default="development",
        help=(
            "validation gate: development checks structure, source checks a "
            "public source tag, and binary adds Windows-runtime license checks"
        ),
    )
    parser.add_argument(
        "--public",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    if args.public:
        if args.artifact != "development":
            parser.error("--public cannot be combined with --artifact")
        args.artifact = "binary"

    errors: list[str] = []
    warnings: list[str] = []
    required = [
        "README.md",
        ".gitattributes",
        ".editorconfig",
        "CHANGELOG.md",
        "CITATION.cff",
        "CONTRIBUTING.md",
        "MANIFEST.in",
        "SECURITY.md",
        "VERSION",
        "pyproject.toml",
        "runtime-manifest.json",
        ".readthedocs.yaml",
        "docs/conf.py",
        "docs/requirements.txt",
        "docs/index.rst",
        "docs/getting_started.rst",
        "docs/windows_application.rst",
        "docs/pfb_pfc_format.rst",
        "docs/python_api.rst",
        "docs/cpp_api.rst",
        "docs/cli.rst",
        "docs/release_scope.rst",
        "docs/en/index.rst",
        "docs/zh_CN/index.rst",
        "docs/PFB_PFC_SPECIFICATION_V1.md",
        "docs/ARCHITECTURE.md",
        "docs/RELEASE_MODEL.md",
        "docs/RELEASE_READINESS_2026-08-20.md",
        "docs/SOURCE_PROVENANCE.md",
        "docs/COMPATIBILITY.md",
        "docs/VALIDATION.md",
        "docs/RUNTIME_DEPENDENCY_AUDIT.md",
        "docs/RELEASE_NOTES_v1.0.0.md",
        "third_party/THIRD_PARTY_NOTICES.template.md",
        "tests/fixtures/minimal.pfb",
        "tests/fixtures/minimal.pfc",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            errors.append(f"missing repository file: {relative}")

    prohibited_suffixes = {".dll", ".exe", ".obj", ".pdb", ".zip"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(ROOT).parts
        if any(part in {".git", "build", "runtime"} for part in relative_parts):
            continue
        if path.suffix.lower() in prohibited_suffixes:
            errors.append(f"binary/archive must not be committed: {path.relative_to(ROOT)}")

    manifest = json.loads((ROOT / "runtime-manifest.json").read_text("utf-8"))
    seen: set[str] = set()
    for entry in manifest["entries"]:
        path = entry["path"]
        if path.lower() in seen:
            errors.append(f"duplicate runtime entry: {path}")
        seen.add(path.lower())
        if args.source_bin and entry.get("required", False):
            if not (args.source_bin / Path(path)).exists():
                errors.append(f"source runtime is missing: {path}")

    version = (ROOT / "VERSION").read_text("utf-8").strip()
    pyproject = (ROOT / "pyproject.toml").read_text("utf-8")
    citation = (ROOT / "CITATION.cff").read_text("utf-8")
    runtime_version = str(manifest.get("release_version", "")).strip()
    if not SEMVER_PATTERN.fullmatch(version):
        errors.append(f"VERSION is not a valid semantic version: {version!r}")
    for name, value in (
        ("pyproject.toml", pyproject),
        ("CITATION.cff", citation),
        ("CHANGELOG.md", (ROOT / "CHANGELOG.md").read_text("utf-8")),
    ):
        if version not in value:
            errors.append(f"VERSION {version} is not synchronized in {name}")
    if runtime_version != version:
        errors.append(
            f"runtime-manifest release_version {runtime_version!r} does not match VERSION {version!r}"
        )

    if not re.search(r"cff-version:\s*1\.2\.0", citation):
        errors.append("CITATION.cff does not declare CFF 1.2.0")

    release_gate = args.artifact in {"source", "binary"}
    if not (ROOT / "LICENSE").is_file():
        message = "source-code LICENSE has not been approved"
        (errors if release_gate else warnings).append(message)
    if "pending" in (ROOT / "CHANGELOG.md").read_text("utf-8").lower():
        message = "release date is still pending"
        (errors if release_gate else warnings).append(message)
    if "repository-code:" not in citation:
        message = "canonical repository URL is not yet present in CITATION.cff"
        (errors if release_gate else warnings).append(message)

    if args.artifact == "binary":
        if args.source_bin is None:
            errors.append("--artifact binary requires --source-bin")
        notices = ROOT / "third_party" / "THIRD_PARTY_NOTICES.txt"
        licenses = ROOT / "third_party" / "licenses"
        if not notices.is_file():
            errors.append("approved third_party/THIRD_PARTY_NOTICES.txt is missing")
        if not licenses.is_dir() or not any(path.is_file() for path in licenses.rglob("*")):
            errors.append("matching third-party license texts are missing")

    print(json.dumps({"errors": errors, "warnings": warnings}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
