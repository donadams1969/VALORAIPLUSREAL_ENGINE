#!/usr/bin/env python3
import json
from pathlib import Path

def clamp(x): return max(0.0, min(1.0, x))

def main(name: str, event: str):
    p = Path("artifacts")/f"agent_{name}.json"
    if not p.exists():
        raise SystemExit("Agent not found. Generate first.")
    agent = json.loads(p.read_text(encoding="utf-8"))
    agent["history"].append(event)

    # Toy update rules
    if "Institutional Betrayal" in event:
        agent["scores"]["moral_injury_index"] = clamp(agent["scores"]["moral_injury_index"] + 0.1)
        agent["scores"]["institutional_trust"] = clamp(agent["scores"]["institutional_trust"] - 0.1)
    if "Supportive Intervention" in event:
        agent["scores"]["resilience_index"] = clamp(agent["scores"]["resilience_index"] + 0.05)
        agent["scores"]["moral_injury_index"] = clamp(agent["scores"]["moral_injury_index"] - 0.05)

    p.write_text(json.dumps(agent, indent=2), encoding="utf-8")
    print(json.dumps(agent, indent=2))

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--event", required=True)
    args = ap.parse_args()
    main(args.name, args.event)
