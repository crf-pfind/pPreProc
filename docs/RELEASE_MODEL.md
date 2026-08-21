# Publication and release model

pPreProc uses one repository but distinguishes online developer documentation
from runnable software releases. This keeps the PFB/PFC contract accessible
without presenting API files as if they were an end-user application package.

## 1. Online interface documentation

Read the Docs is the maintained publication surface for:

- the normative indexed PFB/PFC v1 contract and compatibility boundary;
- the source-visible Python and header-only C++17 reference readers;
- validation, command-line, and integration examples; and
- bilingual English and Simplified Chinese usage documentation.

Documentation builds from the main branch as `latest`. Future software tags
that contain the Sphinx configuration may also be enabled as immutable,
version-specific documentation. These pages and source files are not attached
to a GitHub Release as a separate downloadable product.

The historical `v1.0.0` tag predates the Sphinx site. It remains unchanged for
provenance and should not be enabled as a Read the Docs version.

## 2. Runnable Windows software Release

A GitHub Release is reserved for the pPreProc application. Its Windows ZIP is
built from an authorized runtime using the explicit whitelist in
`runtime-manifest.json`. It contains the user-facing pPreProc entry point and
the compiled components required by the validated workflow, while excluding
the pFind search engine, GUI, reporting tools, logs, debug artifacts, and
unrelated utilities.

The ZIP does not claim that the compiled application implementation is open
source. Publication additionally requires project-owner authorization, exact
third-party notices and license texts, checksums, and validation on a clean
Windows machine. If a vendor library may not be redistributed, the package
must use the vendor's official installer or bootstrap procedure.

## 3. Versioning and citation

The documentation `latest` version follows development. A stable documentation
version corresponds to the same tag as a runnable software Release. Analyses
should record the software tag, platform, input format, command/configuration,
and artifact checksum. After archival, the version DOI should be cited together
with the associated article.

## 4. Wording used in documentation and the manuscript

- **Online/source-visible:** the PFB/PFC specification, Python/C++ readers,
  fixtures, tests, and integration documentation in the repository and on
  Read the Docs.
- **Standalone software:** an authorized Windows application Release that runs
  independently of the pFind search engine and GUI.
- **Not claimed:** that the compiled Windows application is fully open source,
  that every vendor-native metadata attribute is preserved, or that every
  third-party search engine reads PFB/PFC without an adapter.
