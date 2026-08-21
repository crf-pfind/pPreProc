# Public release blockers

The repository source and the Windows runtime asset have different publication
gates. Completing the source-release list does not authorize the binary asset.

## Source tag v1.0.0

- [x] Approve BSD-3-Clause for the repository's original source code.
- [x] Create the canonical public GitHub repository at
      `https://github.com/crf-pfind/pPreProc`.
- [x] Match the author order in `CITATION.cff` to the manuscript; no unconfirmed
      ORCID identifiers are included.
- [x] Run the Python and C++ tests and `validate_release.py --artifact source`.
- [x] Tag the exact source commit as `v1.0.0` on publication.

## Post-publication archival

- [ ] Archive the public source release with Zenodo and add the version DOI.

## Windows runtime asset

- [ ] Confirm that `pParse.exe`, pParse2+, pXtract, model files, and associated
      pFind-owned resources may be redistributed as a standalone package.
- [ ] Confirm and document whether the extracted preprocessing components have
      any pFind activation, license-file, or expiration dependency; verify that
      the standalone entry point behaves as documented on a clean machine.
- [ ] Confirm redistribution terms for Thermo RawFileReader, Bruker timsdata,
      SCIEX Clearcore, SQLite, log4net, Mono.Options, Ionic.Zlib, and Microsoft
      runtime files included by the runtime manifest.
- [ ] Resolve the exact-license status of `Clearcore2.Processing.dll`; it was
      not present in the legacy SCIEX distributable-component list found in
      the audit.
- [ ] Reconstruct the exact version/license inventory for the frozen pParse2+
      Python/OpenSSL/NumPy/pandas runtime, or rebuild it from a locked
      environment that preserves dependency metadata.
- [ ] Replace `third_party/THIRD_PARTY_NOTICES.template.md` with an approved
      `THIRD_PARTY_NOTICES.txt` and place the applicable full license texts in
      `third_party/licenses/`.
- [ ] Decide whether Microsoft runtimes will be installed through official
      VC++ Redistributable prerequisites (recommended) or locally redistributed
      under confirmed Visual Studio license rights.
- [ ] Run `validate_release.py --artifact binary --source-bin <authorized-bin>`.
- [ ] Build the ZIP from the exact source tag and attach its SHA-256 manifest.
- [ ] Verify the final archive on a clean Windows machine.

If redistribution of one or more vendor libraries is not permitted, document
an official installer/bootstrap procedure instead of copying those files into
the release archive.
