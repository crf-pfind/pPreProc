# Documentation maintenance

The documentation is a bilingual Sphinx site. English and Simplified Chinese
use the same source repository and configuration, but are built as two linked
Read the Docs projects so that Read the Docs can provide its standard language
switcher and language-specific URLs.

## Local builds

From the repository root in PowerShell:

```powershell
python -m pip install -r docs/requirements.txt
python -m pip install .

sphinx-build -W --keep-going -b html docs docs/_build/en

sphinx-build -W --keep-going -t zh-cn -b html docs docs/_build/zh-cn
```

The CI workflow performs both builds for every pull request and push.

## Read the Docs project setup

Import the same GitHub repository twice in Read the Docs:

1. Create the English project, preferably with the slug `ppreproc`, and set
   its language to English.
2. Create the Chinese project, preferably with the slug `ppreproc-zh-cn`, and
   set its language to Simplified Chinese.
3. In the Chinese project, open **Admin > Advanced settings** and set
   **Translation of** to the English project.
4. Build `latest` in both projects. The repository-level
   `.readthedocs.yaml` selects `docs/conf.py`; the Read the Docs-provided
   `READTHEDOCS_LANGUAGE` variable selects the correct source tree.
5. Keep the historical `v1.0.0` documentation version inactive because that
   tag predates the Sphinx configuration. Future software tags can be enabled
   as versioned documentation after their builds pass.

Once imported, the intended public routes are:

- English: `https://ppreproc.readthedocs.io/en/latest/`
- Simplified Chinese: `https://ppreproc.readthedocs.io/zh-cn/latest/`

If the preferred Read the Docs slug is unavailable, update the documentation
links in `README.md` and `pyproject.toml` after choosing the final slug.

## Publication boundary

API references, the PFB/PFC format contract, and usage guides are maintained
as online documentation. They are not packaged as GitHub Release assets.
GitHub Releases are reserved for runnable, versioned pPreProc software and its
required notices/checksums after the Windows redistribution gate is complete.
