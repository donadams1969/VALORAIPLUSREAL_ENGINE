#!/usr/bin/env python3
# Local JSON 'anchoring' fallback for offline dev.

import json, time, hashlib
from pathlib import Path

LEDGER = Path("artifacts/sovereign_ledger.json")

def sha256_bytes(b: bytes) -> str:
    import hashlib
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

def commit(kind: str, metadata: dict) -> dict:
    rec = {
        "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "kind": kind,
        "metadata": metadata,
    }
    rec_bytes = json.dumps(rec, sort_keys=True).encode("utf-8")
    rec_hash = sha256_bytes(rec_bytes)
    ledger = []
    if LEDGER.exists():
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger.append({"hash": rec_hash, "record": rec})
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return {"hash": rec_hash, "record": rec}
