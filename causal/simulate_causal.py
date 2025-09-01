#!/usr/bin/env python3
# Simple SCM simulator with do-operator interventions and narrative summarizer.

import json, random
from pathlib import Path

def load_graph(path):
    g = json.loads(Path(path).read_text(encoding="utf-8"))
    return g  # {"nodes":[...], "edges":[["A","B"]], "equations":{"B":"0.7*A+eps"}}

def simulate(graph, steps=24, do_intervention=None, seed=777):
    rnd = random.Random(seed)
    nodes = graph["nodes"]
    edges = graph["edges"]
    eq = graph.get("equations", {})
    state = {n: 0.0 for n in nodes}
    trace = []

    # Parse do-intervention "X=1"
    do = {}
    if do_intervention:
        for part in do_intervention.split(","):
            k, v = part.split("=")
            do[k.strip()] = float(v.strip())

    for t in range(steps):
        new_state = state.copy()
        for n in nodes:
            if n in do:
                new_state[n] = do[n]  # intervention
                continue
            expr = eq.get(n, "0.9*{n}+eps".format(n=n))
            val = eval(expr, {"__builtins__":{}}, {**state, "eps": rnd.uniform(-0.05,0.05)})
            new_state[n] = float(val)
        state = new_state
        trace.append({"t": t, **state})
    return trace

def narrate(trace, key="Outcome"):
    vals = [step[key] for step in trace if key in step]
    if not vals:
        return "No outcome tracked."
    trend = "increasing" if vals[-1] > vals[0] else "decreasing"
    return f"Outcome {trend} from {vals[0]:.3f} to {vals[-1]:.3f} over {len(vals)} steps."

def main(graph_path, do_str, steps):
    g = load_graph(graph_path)
    tr = simulate(g, steps=steps, do_intervention=do_str)
    outdir = Path("artifacts"); outdir.mkdir(parents=True, exist_ok=True)
    (outdir/"causal_trace.json").write_text(json.dumps(tr, indent=2), encoding="utf-8")
    summary = narrate(tr, key=g.get("outcome","Outcome"))
    (outdir/"causal_summary.txt").write_text(summary, encoding="utf-8")
    print(summary)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True)
    ap.add_argument("--do", default=None)
    ap.add_argument("--steps", type=int, default=24)
    args = ap.parse_args()
    main(args.graph, args.do, args.steps)
