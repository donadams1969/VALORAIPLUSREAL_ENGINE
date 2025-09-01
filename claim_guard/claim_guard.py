#!/usr/bin/env python3
import sys, re, json
from pathlib import Path

DISALLOWED = [
    r"we\s+solved\s+3d\s+navier[\-\s]*stokes\s+global\s+regularity",
    r"peer\s+review\s+is\s+unnecessary",
    r"quantum|sgai.*overrides.*need.*proof"
]

SCOPE_REGEX = re.compile(r"does\s+not\s+claim", re.IGNORECASE)

def files():
    exts = {".md",".txt",".py",".sol",".json",".yml",".yaml",".tex"}
    for p in Path(".").rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            if any(part in {".git",".venv","node_modules","__pycache__"} for part in p.parts):
                continue
            yield p

def main()->int:
    bad=[]; scope=False
    for p in files():
        t = p.read_text(encoding="utf-8", errors="ignore")
        if SCOPE_REGEX.search(t): scope=True
        low = t.lower()
        for pat in DISALLOWED:
            if re.search(pat, low):
                bad.append(str(p))
    print(json.dumps({"scope_found":scope,"violations":bad}, indent=2))
    if not scope: print("Missing scope statement.", file=sys.stderr); return 2
    if bad: print("Disallowed claim(s) found.", file=sys.stderr); return 3
    return 0

if __name__=="__main__":
    sys.exit(main())
