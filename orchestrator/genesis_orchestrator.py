#!/usr/bin/env python3
import json, time
from pathlib import Path

REGISTRY = {
    "ledger": "ledger/local_ledger.py",
    "digital_soul": "digital_soul",
    "veracity": "veracity",
    "causal": "causal",
}

def main():
    print("[Genesis Orchestrator] registry loaded:", json.dumps(REGISTRY, indent=2))
    print("This is a lightweight supervisor stub. Extend with process mgmt, queues, and policy.")
    Path("artifacts").mkdir(exist_ok=True, parents=True)
    (Path("artifacts") / "orchestrator_heartbeat.json").write_text(
        json.dumps({"ts": time.time(), "status":"ok"}), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
