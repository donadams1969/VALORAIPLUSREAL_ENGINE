from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict

def write_json(obj: Dict[str, Any], outdir: Path, name: str) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    p = outdir / name
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return p
