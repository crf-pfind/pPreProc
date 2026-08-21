# Python PFB/PFC SDK

`ppreproc_pfb` is the dependency-free Python reference implementation of the
indexed PFB/PFC v1 interface.

Install it from the repository root with `python -m pip install .`. The public
API consists of `PFBReader`, `PFBRecord`, and `PFBFormatError`; installation
also provides the `ppreproc-pfb` validation CLI.

See the [Python SDK documentation](https://ppreproc.readthedocs.io/en/latest/reference/python-api.html)
and `tests/` for supported behavior. A minimal script is available in
`examples/read_spectrum.py`.
