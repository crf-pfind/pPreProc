"""Sphinx configuration shared by the English and Chinese documentation."""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

project = "pPreProc"
author = "pPreProc developers"
copyright = "2026, pPreProc developers"
release = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_numpy_docstring = True
napoleon_google_docstring = True

language_from_environment = os.environ.get("READTHEDOCS_LANGUAGE", "en")
normalized_language = language_from_environment.lower().replace("_", "-")
is_chinese = tags.has("zh-cn") or normalized_language in {"zh", "zh-cn", "zh-hans"}

language = "zh_CN" if is_chinese else "en"
root_doc = "index"
exclude_patterns = [
    "_build",
    "*.md",
    "en/**",
    "zh_CN/**",
]

html_theme = "sphinx_rtd_theme"
html_title = (
    f"pPreProc {release} 文档"
    if is_chinese
    else f"pPreProc {release} documentation"
)
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "sticky_navigation": True,
}
html_context = {
    "display_github": True,
    "github_user": "crf-pfind",
    "github_repo": "pPreProc",
    "github_version": "main",
    "conf_py_path": "/docs/",
}


TRANSLATED_PAGES = {
    "index",
    "getting_started",
    "windows_application",
    "pfb_pfc_format",
    "python_api",
    "cpp_api",
    "cli",
    "release_scope",
}


def _select_language_source(app, docname, source):
    """Replace each shared route with its selected language source."""

    if docname not in TRANSLATED_PAGES:
        return
    language_directory = "zh_CN" if is_chinese else "en"
    source_path = Path(__file__).parent / language_directory / f"{docname}.rst"
    source[0] = source_path.read_text(encoding="utf-8")


def setup(app):
    app.connect("source-read", _select_language_source)
