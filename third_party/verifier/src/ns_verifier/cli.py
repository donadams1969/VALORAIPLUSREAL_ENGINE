from __future__ import annotations
import argparse, os, json
from pathlib import Path
from typing import Any, Dict

from .backends import get_xp, is_gpu
from .projection import projection_check
from .intervals import small_interval_checks
from .attest import write_manifest
from .report import write_json

def load_plugins(registry: Dict[str, Any]) -> None:
    plugin_path = os.environ.get("NS_VERIFIER_PLUGIN_PATH")
    if not plugin_path:
        return
    p = Path(plugin_path)
    for modfile in p.glob("*.py"):
        name = modfile.stem
        spec = {"__file__": str(modfile)}
        code = compile(modfile.read_text(encoding="utf-8"), str(modfile), "exec")
        local_ns: Dict[str, Any] = {}
        exec(code, {}, local_ns)
        if "register" in local_ns and callable(local_ns["register"]):
            local_ns["register"](registry)

def main() -> None:
    ap = argparse.ArgumentParser(prog="nsverify", description="Engineer modular verifier for projection/Poisson step.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_proj = sub.add_parser("projection", help="Run projection/Poisson equivalence check")
    ap_proj.add_argument("--nx", type=int, default=64)
    ap_proj.add_argument("--ny", type=int, default=64)
    ap_proj.add_argument("--nz", type=int, default=64)
    ap_proj.add_argument("--dt", type=float, default=1e-2)
    ap_proj.add_argument("--gpu", action="store_true")
    ap_proj.add_argument("--outdir", default="artifacts")

    ap_iv = sub.add_parser("intervals", help="Run small interval arithmetic checks")
    ap_iv.add_argument("--outdir", default="artifacts")

    ap_mf = sub.add_parser("manifest", help="Build manifest and SHA256 map")
    ap_mf.add_argument("--root", default=".")
    ap_mf.add_argument("--outdir", default="artifacts")

    # Plugins
    ap_pl = sub.add_parser("plugins", help="Run registered plugins")
    ap_pl.add_argument("--outdir", default="artifacts")

    args = ap.parse_args()
    if args.cmd == "projection":
        xp = get_xp(args.gpu)
        metrics = projection_check(xp, args.nx, args.ny, args.nz, dt=args.dt)
        metrics["gpu"] = bool(args.gpu) and is_gpu(xp)
        write_json(metrics, Path(args.outdir), "projection_metrics.json")
        print(json.dumps(metrics, indent=2))

    elif args.cmd == "intervals":
        out = small_interval_checks()
        write_json(out, Path(args.outdir), "interval_checks.json")
        print(json.dumps(out, indent=2))

    elif args.cmd == "manifest":
        root = Path(args.root).resolve()
        outdir = Path(args.outdir)
        mapping = write_manifest(root, outdir / "MANIFEST_SHA256.txt", outdir / "manifest.json")
        print(f"Wrote manifest for {len(mapping)} files under {root}")

    elif args.cmd == "plugins":
        registry: Dict[str, Any] = {}
        load_plugins(registry)
        outdir = Path(args.outdir)
        results: Dict[str, Any] = {}
        for name, fn in registry.items():
            try:
                results[name] = fn()
            except Exception as e:  # robust reporting
                results[name] = {"error": str(e)}
        write_json(results, outdir, "plugin_results.json")
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
