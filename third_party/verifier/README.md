# NS Engineer Modular Verifier (v1)

A small, **engineer-friendly** Python package for verifying the **projection / pressure–Poisson** step used in many incompressible Navier–Stokes solvers. It’s modular, typed, testable, and ships with a CLI and plugin hooks so other engineers can re-run and extend the verification.

**Scope:** This package **does not** prove 3D Navier–Stokes global regularity. It verifies the correctness of the projection method (via FFT/Hodge) and provides reproducible metrics/artifacts.

## Features
- Clean modules (`ns_verifier/*`) with type hints
- CPU (NumPy) by default; optional GPU (CuPy) backend
- CLI: `nsverify` for running checks and producing JSON artifacts
- Plugin hook via `NS_VERIFIER_PLUGIN_PATH`
- Pytest unit tests
- Manifest + SHA256 attestation
- Optional interval arithmetic (mpmath)

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
nsverify projection --nx 64 --ny 64 --nz 64 --steps 3
nsverify intervals
nsverify manifest
```

Artifacts are written to `artifacts/` and include logs suitable for signing.

## Plugins
Set `NS_VERIFIER_PLUGIN_PATH=/path/to/plugins` and drop in modules exporting a `register(plugin_registry)` function. See `plugins/sample_plugin.py` for a template.

## License
MIT
