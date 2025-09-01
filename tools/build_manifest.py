#!/usr/bin/env python3
import argparse, json, hashlib
from pathlib import Path

def sha256_of_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Directory to hash")
    ap.add_argument("--out", default="artifacts", help="Directory for outputs")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)

    mapping = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            mapping[str(p.relative_to(root))] = sha256_of_file(p)

    (out/"MANIFEST_SHA256.txt").write_text(
        "\n".join(f"{v}  {k}" for k,v in mapping.items()) + "\n", encoding="utf-8"
    )
    (out/"manifest.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print(f"Hashed {len(mapping)} files under {root}.")

if __name__ == "__main__":
    main()
