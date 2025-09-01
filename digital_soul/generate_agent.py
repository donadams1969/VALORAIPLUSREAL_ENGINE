#!/usr/bin/env python3
import json, random
from pathlib import Path

def clamp(x): return max(0.0, min(1.0, x))

def main(name: str):
    rnd = random.Random(name)
    agent = {
        "name": name,
        "traits": {
            "conscientiousness": clamp(rnd.uniform(0.3, 0.9)),
            "agreeableness":     clamp(rnd.uniform(0.2, 0.9)),
            "neuroticism":       clamp(rnd.uniform(0.1, 0.8)),
            "openness":          clamp(rnd.uniform(0.3, 0.95)),
            "extraversion":      clamp(rnd.uniform(0.2, 0.9)),
        },
        "history": [],
        "scores": {
            "resilience_index": clamp(rnd.uniform(0.4, 0.7)),
            "moral_injury_index": clamp(rnd.uniform(0.1, 0.3)),
            "institutional_trust": clamp(rnd.uniform(0.2, 0.8))
        }
    }
    Path("artifacts").mkdir(parents=True, exist_ok=True)
    (Path("artifacts")/f"agent_{name}.json").write_text(json.dumps(agent, indent=2), encoding="utf-8")
    print(json.dumps(agent, indent=2))

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    args = ap.parse_args()
    main(args.name)
