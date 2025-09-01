#!/usr/bin/env python3
import argparse
from pathlib import Path
from ed25519_sign import sign

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keys", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", default="artifacts")
    args = ap.parse_args()
    keys = Path(args.keys); manifest = Path(args.manifest)
    Path(args.out).mkdir(parents=True, exist_ok=True)
    sign(keys / "private.key", manifest, Path(args.out) / (manifest.name + ".sig"))

if __name__ == "__main__":
    main()
