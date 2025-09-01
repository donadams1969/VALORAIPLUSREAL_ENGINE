# VALOR Genesis Engine — Alpha Kit (v1)

**Purpose:** A merged, offline‑ready starter kit for **Hyper‑Veracity Simulation** that aligns with your
VALOR AI+ pillars and the ValorAiMathAVM workbench discipline (attestation, CI guards, manifests).

**Core pillars implemented here:**
1) **Consequence Architecture (Sovereign Lock):** cryptographic persistence of actions with Solidity contract stub
   + local JSON ledger fallback; each action → SHA‑256 → signed (Ed25519) → anchor stub.
2) **Digital Soul Core:** schemas + generator for psychologically rich agents (trauma/resilience/moral‑injury indices).
3) **Veracity Layer:** evidentiary ingestion → “Digital Witness Scene” assembly + **Chronos‑Anchor** (OTS‑style timestamps).
4) **Quantum Causal Inference:** structural causal model (SCM) with do‑interventions; narrative generator for long‑horizon impact.
5) **Orchestrator + CLI:** uniform entrypoints to commit actions, ingest evidence, run causal sims, and produce artifact cards.
6) **Attestation:** manifests + Ed25519 signing; **Claim Guard** to block overclaims in PRs.
7) **CI Skeleton:** GitHub Actions workflow mirroring the ValorAiMathAVM research pipeline.

> This alpha kit does **not** claim 3D Navier–Stokes global regularity or court‑admissible evidence by itself.
> It gives you a verifiable, extensible foundation to build those capabilities honestly and rigorously.

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1) Commit an irreversible action (local ledger + signature)
python cli/commit_action.py --actor "UnitTest" --kind DECISION --details "Approved policy X"

# 2) Create a Digital Soul profile and update it after an event
python digital_soul/generate_agent.py --name "PatientZero"
python digital_soul/update_agent.py --name "PatientZero" --event "Institutional Betrayal"

# 3) Ingest evidence and build a Digital Witness Scene + timestamp
python veracity/ingest_evidence.py --src samples/evidence_sample.json

# 4) Run a causal simulation with an intervention
python causal/simulate_causal.py --graph samples/causal_graph.json --do "PolicyBlock=1" --steps 24

# 5) Build manifest + artifact card and (optionally) sign
python tools/build_manifest.py --root . --out artifacts
python tools/ed25519_sign.py keygen --out keys
python tools/sign_manifest.py --keys keys --manifest artifacts/MANIFEST_SHA256.txt --out artifacts
python tools/build_artifact_card.py --out artifacts
```

## Directory Map
- `orchestrator/` — engine runtime supervisor (Python), registry, and config.
- `ledger/` — **SovereignLock.sol** (stub) + local JSON ledger adapter.
- `digital_soul/` — agent schemas, generator, updater (moral‑injury, resilience).
- `veracity/` — evidence ingestion → scene graph; OTS‑style timestamping.
- `causal/` — structural causal model + do‑operator simulator + narrative.
- `cli/` — command‑line tools to exercise the system.
- `tools/` — manifests, signing, artifact cards.
- `claim_guard/` + `.github/workflows/` — CI gate + pipeline.
- `samples/` — minimal example data.

## Scope statement (include in your repos)
This engine provides **verifiable components** (consequence ledger, digital‑soul schemas, evidence scenes, causal sims)
and a disciplined pipeline (manifests, signatures, claim guard). It **does not** claim global regularity or legal admissibility
without independent, peer‑reviewed validation and jurisdiction‑specific requirements.
