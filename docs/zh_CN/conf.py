from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "sdk" / "python" / "src"))

project = "pPreProc"
author = "pPreProc developers"
copyright = "2026, pPreProc developers"
release = (ROOT / "SDK_VERSION").read_text(encoding="utf-8").strip()
version = release
language = "zh_CN"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_numpy_docstring = True
napoleon_google_docstring = True

root_doc = "index"
exclude_patterns = ["_build"]
html_theme = "sphinx_rtd_theme"
html_title = "pPreProc 文档"
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
    "conf_py_path": "/docs/zh_CN/",
}
