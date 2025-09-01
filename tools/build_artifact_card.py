#!/usr/bin/env python3
import argparse, json, hashlib, time
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)

    card = {
        "name": "VALOR Genesis Engine — Alpha Kit",
        "version": "v1",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "artifacts": {}
    }
    for name in ["sovereign_ledger.json", "causal_trace.json", "manifest.json", "MANIFEST_SHA256.txt"]:
        p = out / name
        if p.exists():
            card["artifacts"][name] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "size": p.stat().st_size}
    (out / "artifact_card.json").write_text(json.dumps(card, indent=2), encoding="utf-8")
    print(json.dumps(card, indent=2))

if __name__ == "__main__":
    main()
