# Release checklist

## Online documentation

1. Build both languages locally with the commands in `docs/README.md`.
2. Require the bilingual documentation workflow to pass without warnings.
3. Keep the English and Chinese table of contents and public API coverage in
   sync.
4. For a new software tag, enable the matching Read the Docs version only
   after both language builds pass.
5. Verify the permanent documentation URLs used by the manuscript and
   reviewer response.

## Windows runtime asset

1. Resolve every Windows-asset item in `RELEASE_BLOCKERS.md`.
2. Validate the authorized runtime directory with `--artifact binary` and
   `--source-bin`.
3. Build the archive using the explicit manifest and inspect it for unrelated
   pFind programs.
4. Test preprocessing and PFB/PFC reading on a clean Windows machine.
5. Create the versioned GitHub Release and attach the ZIP and SHA-256 manifest.
6. Confirm that the same tag builds the stable English and Chinese online
   documentation; do not attach API/specification files as Release assets.
