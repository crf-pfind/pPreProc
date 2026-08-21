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

PROHIBITED_CHINESE_TERMS = {
    "母谱": "一级谱",
    "子谱": "二级谱",
    "前体": "母离子",
}


def _required_files() -> list[str]:
    return [
        ".github/CODE_OF_CONDUCT.md",
        ".github/CONTRIBUTING.md",
        ".github/RELEASING.md",
        ".github/SECURITY.md",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/documentation.yml",
        ".gitattributes",
        ".gitignore",
        ".readthedocs.yaml",
        "CITATION.cff",
        "LICENSE",
        "README.md",
        "pyproject.toml",
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
        "sdk/python/examples/read_spectrum.py",
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

    allowed_root_files = {
        ".gitattributes",
        ".gitignore",
        ".readthedocs.yaml",
        "CITATION.cff",
        "LICENSE",
        "README.md",
        "pyproject.toml",
    }
    root_files = {path.name for path in ROOT.iterdir() if path.is_file()}
    for name in sorted(root_files - allowed_root_files):
        errors.append(f"unexpected root file: {name}")

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    project_section = re.search(
        r"(?ms)^\[project\]\s*$\n(.*?)(?=^\[|\Z)", pyproject
    )
    version_match = (
        re.search(r'(?m)^version\s*=\s*"([^"]+)"\s*$', project_section.group(1))
        if project_section
        else None
    )
    sdk_version = version_match.group(1) if version_match else ""
    if not SEMVER.fullmatch(sdk_version):
        errors.append(f"invalid project version: {sdk_version!r}")

    format_root = ROOT / "interfaces/pfb-pfc"
    format_versions = sorted(
        int(path.name[1:])
        for path in format_root.iterdir()
        if path.is_dir() and re.fullmatch(r"v[1-9]\d*", path.name)
    )
    if not format_versions:
        errors.append("no versioned PFB/PFC specification found")
        format_version = 0
    else:
        format_version = format_versions[-1]

    synchronized = {
        "pyproject.toml": pyproject,
        "Python SDK": (
            ROOT / "sdk/python/src/ppreproc_pfb/__init__.py"
        ).read_text(encoding="utf-8"),
        "C++ SDK": (ROOT / "sdk/cpp/CMakeLists.txt").read_text(encoding="utf-8"),
        "CITATION.cff": (ROOT / "CITATION.cff").read_text(encoding="utf-8"),
    }
    for name, content in synchronized.items():
        if sdk_version not in content:
            errors.append(f"SDK version {sdk_version} is not synchronized in {name}")

    specification = (
        ROOT / f"interfaces/pfb-pfc/v{format_version}/specification.md"
    ).read_text(encoding="utf-8")
    if f"Format version: {format_version}" not in specification:
        errors.append("format directory and specification version are not synchronized")

    english = _document_paths("en")
    chinese = _document_paths("zh_CN")
    for missing in sorted(english - chinese):
        errors.append(f"Chinese documentation is missing: {missing}")
    for missing in sorted(chinese - english):
        errors.append(f"English documentation is missing: {missing}")

    for path in sorted((ROOT / "docs" / "zh_CN").rglob("*.rst")):
        content = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT).as_posix()
        for prohibited, preferred in PROHIBITED_CHINESE_TERMS.items():
            for line_number, line in enumerate(content.splitlines(), start=1):
                if prohibited in line:
                    errors.append(
                        f"nonstandard Chinese term {prohibited!r} in "
                        f"{relative}:{line_number}; use {preferred!r}"
                    )

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
    if manifest.get("schema_version") != 2:
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
        source_root = entry.get("source_root", "application")
        if source_root not in {"application", "microsoft_vc"}:
            errors.append(f"unsupported runtime source root: {source_root}")

    release_evidence = [
        ROOT / "distribution/windows/APPLICATION_LICENSE.txt",
        ROOT / "distribution/windows/runtime-provenance.json",
        ROOT / "distribution/windows/third-party/THIRD_PARTY_NOTICES.txt",
        ROOT / "distribution/windows/third-party/third-party-components.json",
        ROOT / "distribution/windows/third-party/licenses/Apache-2.0.txt",
    ]
    for path in release_evidence:
        if not path.is_file():
            errors.append(f"release evidence is missing: {path.relative_to(ROOT)}")

    print(json.dumps({"errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
