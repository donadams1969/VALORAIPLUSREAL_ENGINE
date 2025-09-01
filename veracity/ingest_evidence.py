#!/usr/bin/env python3
# Build a "Digital Witness Scene" from an evidence JSON file and timestamp it (OTS-style).

import json, time, hashlib
from pathlib import Path

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

def main(src: str):
    data = json.loads(Path(src).read_text(encoding="utf-8"))
    scene = {
        "scene_id": sha256_bytes(Path(src).read_bytes())[:16],
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "entities": data.get("entities", []),
        "events": data.get("events", []),
        "links": data.get("links", [])
    }
    Path("artifacts").mkdir(parents=True, exist_ok=True)
    out = Path("artifacts")/f"scene_{scene['scene_id']}.json"
    out.write_text(json.dumps(scene, indent=2), encoding="utf-8")

    # Chronos-Anchor: minimal OTS-style proof (local)
    ots = {
        "scene_id": scene["scene_id"],
        "hash": sha256_bytes(out.read_bytes()),
        "timestamp_utc": scene["timestamp_utc"]
    }
    (Path("artifacts")/f"scene_{scene['scene_id']}.ots.json").write_text(json.dumps(ots, indent=2), encoding="utf-8")
    print(json.dumps({"scene": scene, "ots": ots}, indent=2))

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    args = ap.parse_args()
    main(args.src)
