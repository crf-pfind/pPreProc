# Examples

Install the Python SDK from the repository root before running an example.

```console
python -m pip install .
python examples/python/read_spectrum.py \
    sdk/python/tests/fixtures/minimal.pfb 102
```

The bundled fixture is synthetic and contains no vendor data. The C++ example
is maintained with the header-only SDK under `sdk/cpp/examples/`.
