# Release checklist

## Source tag

1. Resolve the source-tag items in `RELEASE_BLOCKERS.md`.
2. Run Python unit tests and C++ example tests on the synthetic fixture.
3. Run full PFB/PFC validation on at least one output from each supported
   instrument family.
4. Run `python tools/validate_release.py --artifact source`.
5. Update `CHANGELOG.md`, `CITATION.cff`, repository URL, and release date.
6. Tag the exact commit as `v1.0.0`.
7. Archive the source tag with Zenodo and record the version DOI.
8. Replace provisional manuscript/reviewer-response wording with the permanent
   URL, DOI, version, and access date.

## Windows runtime asset

1. Resolve every Windows-asset item in `RELEASE_BLOCKERS.md`.
2. Validate the authorized runtime directory with `--artifact binary` and
   `--source-bin`.
3. Build the archive using the explicit manifest and inspect it for unrelated
   pFind programs.
4. Test preprocessing and PFB/PFC reading on a clean Windows machine.
5. Attach the ZIP and SHA-256 manifest to the matching versioned release.
