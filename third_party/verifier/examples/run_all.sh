#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
nsverify projection --nx 32 --ny 32 --nz 32 --steps 2
nsverify intervals
nsverify manifest --root .
pytest -q
echo 'All good.'
