# Release process

GitHub Releases are reserved for runnable pPreProc application packages. SDK
and format changes are maintained in the repository and versioned
independently.

## Required assets

For a Windows application release `X.Y.Z`, publish:

- `pPreProc-X.Y.Z-windows-x64.zip`;
- `pPreProc-X.Y.Z-windows-x64.zip.sha256`;
- user-facing release notes.

The archive must contain application terms, public-component and third-party
notices, the runtime manifest, and `SHA256SUMS.txt`.

## Release gate

1. Confirm the application version and compatibility matrix.
2. Review redistribution rights for every runtime-manifest entry.
3. Complete the application license and third-party notice bundle.
4. Run all SDK, format, and documentation checks.
5. Build the archive from an authorized runtime:

   ```powershell
   .\tools\build_windows_release.ps1 `
       -Version X.Y.Z `
       -SourceBin D:\path\to\authorized\bin `
       -VCRuntimeDirectory 'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Redist\MSVC\14.38.33130\x64' `
       -AcknowledgeRedistributionRights
   ```

6. Test the exact archive on a clean supported Windows system.
7. Verify conversion, configuration loading, output validation, and checksums.
8. Create a draft GitHub Release and attach all assets before publication.

## Release notes

Write for software users, not repository maintainers. Use this order:

1. Highlights
2. Installation or upgrade instructions
3. Compatibility
4. Improvements
5. Fixes
6. Breaking changes
7. Known issues
8. Checksums and documentation links

Do not publish an application tag or Release when only source archives are
available.
