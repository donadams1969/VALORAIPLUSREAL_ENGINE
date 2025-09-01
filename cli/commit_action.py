#!/usr/bin/env python3
import json, argparse
from pathlib import Path
from ledger.local_ledger import commit

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--actor", required=True)
    ap.add_argument("--kind", required=True, help="DECISION|ACTION|EVIDENCE|POLICY")
    ap.add_argument("--details", required=True)
    args = ap.parse_args()
    res = commit(args.kind, {"actor": args.actor, "details": args.details})
    Path("artifacts").mkdir(parents=True, exist_ok=True)
    (Path("artifacts")/"last_action.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
