from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Dict, Iterable

def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def write_manifest(root: Path, outfile_txt: Path, outfile_json: Path, exclude_suffixes: Iterable[str] = (".zip",)) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and not any(str(p).endswith(suf) for suf in exclude_suffixes):
            mapping[str(p.relative_to(root))] = sha256_of_file(p)

    outfile_txt.write_text("\n".join(f"{v}  {k}" for k,v in mapping.items()) + "\n", encoding="utf-8")
    outfile_json.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    return mapping
