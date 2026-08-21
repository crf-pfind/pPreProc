"""Check the public repository structure and version contracts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)


def _required_files() -> list[str]:
    return [
        ".github/RELEASING.md",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/documentation.yml",
        ".github/ISSUE_TEMPLATE/sdk_bug.yml",
        ".readthedocs.yaml",
        "CHANGELOG.md",
        "CITATION.cff",
        "CODE_OF_CONDUCT.md",
        "COMPATIBILITY.md",
        "CONTRIBUTING.md",
        "FORMAT_VERSION",
        "LICENSE",
        "NOTICE",
        "README.md",
        "SDK_VERSION",
        "SECURITY.md",
        "SUPPORT.md",
        "distribution/windows/README.md",
        "distribution/windows/PACKAGE_README.md",
        "distribution/windows/runtime-manifest.json",
        "docs/en/conf.py",
        "docs/en/index.rst",
        "docs/zh_CN/.readthedocs.yaml",
        "docs/zh_CN/conf.py",
        "docs/zh_CN/index.rst",
        "interfaces/pfb-pfc/v1/specification.md",
        "sdk/cpp/CMakeLists.txt",
        "sdk/cpp/include/ppreproc/pfb_reader.hpp",
        "sdk/python/src/ppreproc_pfb/__init__.py",
        "sdk/python/tests/fixtures/minimal.pfb",
        "sdk/python/tests/fixtures/minimal.pfc",
    ]


def _document_paths(language: str) -> set[str]:
    source = ROOT / "docs" / language
    return {
        path.relative_to(source).as_posix()
        for path in source.rglob("*.rst")
    }


def main() -> int:
    errors: list[str] = []

    for relative in _required_files():
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    sdk_version = (ROOT / "SDK_VERSION").read_text(encoding="utf-8").strip()
    format_version = (ROOT / "FORMAT_VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(sdk_version):
        errors.append(f"invalid SDK_VERSION: {sdk_version!r}")
    if not format_version.isdigit() or int(format_version) < 1:
        errors.append(f"invalid FORMAT_VERSION: {format_version!r}")

    synchronized = {
        "pyproject.toml": (ROOT / "pyproject.toml").read_text(encoding="utf-8"),
        "Python SDK": (
            ROOT / "sdk/python/src/ppreproc_pfb/__init__.py"
        ).read_text(encoding="utf-8"),
        "C++ SDK": (ROOT / "sdk/cpp/CMakeLists.txt").read_text(encoding="utf-8"),
        "CITATION.cff": (ROOT / "CITATION.cff").read_text(encoding="utf-8"),
    }
    for name, content in synchronized.items():
        if sdk_version not in content:
            errors.append(f"SDK_VERSION {sdk_version} is not synchronized in {name}")

    specification = (
        ROOT / "interfaces/pfb-pfc/v1/specification.md"
    ).read_text(encoding="utf-8")
    if f"Format version: {format_version}" not in specification:
        errors.append("FORMAT_VERSION is not synchronized in the specification")

    english = _document_paths("en")
    chinese = _document_paths("zh_CN")
    for missing in sorted(english - chinese):
        errors.append(f"Chinese documentation is missing: {missing}")
    for missing in sorted(chinese - english):
        errors.append(f"English documentation is missing: {missing}")

    prohibited_suffixes = {".dll", ".exe", ".obj", ".pdb", ".zip"}
    ignored_parts = {".git", "build", "runtime", "__pycache__"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in ignored_parts for part in relative.parts):
            continue
        if path.suffix.lower() in prohibited_suffixes:
            errors.append(f"binary or archive is committed: {relative.as_posix()}")

    manifest_path = ROOT / "distribution/windows/runtime-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        errors.append("unsupported runtime-manifest schema_version")
    seen: set[str] = set()
    for entry in manifest.get("entries", []):
        relative = str(entry.get("path", "")).strip()
        normalized = relative.lower()
        if not relative:
            errors.append("runtime-manifest entry has an empty path")
        elif normalized in seen:
            errors.append(f"duplicate runtime-manifest entry: {relative}")
        seen.add(normalized)
        if "required" not in entry or "category" not in entry:
            errors.append(f"incomplete runtime-manifest entry: {relative}")

    print(json.dumps({"errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
