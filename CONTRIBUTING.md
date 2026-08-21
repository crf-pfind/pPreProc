# Contributing

Bug reports should include the pPreProc version, operating system, input file
type, exact command, and the smallest reproducible example permitted by the
data owner. Do not upload proprietary vendor files without authorization.

For code changes:

1. Create a focused branch and keep unrelated formatting changes separate.
2. Add or update a test for any changed PFB/PFC behavior.
3. Run `python -m unittest discover -s tests -v`.
4. Run `python tools/validate_release.py`; release maintainers additionally run
   `--artifact source` or `--artifact binary` for the relevant deliverable.
5. Update `CHANGELOG.md` when behavior visible to users changes.

Changes to the PFB/PFC byte layout require a new format version and a new
specification document. Existing v1 files must remain readable.
