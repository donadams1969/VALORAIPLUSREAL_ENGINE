#!/usr/bin/env python3
# Minimal Ed25519 signing util (requires pynacl or cryptography).
import argparse, sys
from pathlib import Path

try:
    from nacl.signing import SigningKey, VerifyKey  # type: ignore
    impl = "pynacl"
except Exception:
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
        from cryptography.hazmat.primitives import serialization
        impl = "cryptography"
    except Exception:
        sys.stderr.write("Install 'pynacl' or 'cryptography' to use this tool.\n")
        sys.exit(1)

def keygen(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    if impl == "pynacl":
        sk = SigningKey.generate(); pk = sk.verify_key
        (outdir/"private.key").write_bytes(sk.encode())
        (outdir/"public.key").write_bytes(pk.encode())
    else:
        sk = Ed25519PrivateKey.generate(); pk = sk.public_key()
        (outdir/"private.key").write_bytes(
            sk.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        (outdir/"public.key").write_bytes(pk.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ))
    print(f"Generated keys in {outdir}")

def sign(priv: Path, file: Path, out: Path):
    data = file.read_bytes()
    if impl == "pynacl":
        sig = SigningKey(priv.read_bytes()).sign(data).signature
    else:
        sig = Ed25519PrivateKey.from_private_bytes(priv.read_bytes()).sign(data)
    out.write_bytes(sig); print(f"Signed {file} -> {out}")

def verify(pub: Path, file: Path, sig: Path):
    data = file.read_bytes(); sigb = sig.read_bytes()
    if impl == "pynacl":
        VerifyKey(pub.read_bytes()).verify(data, sigb)
    else:
        Ed25519PublicKey.from_public_bytes(pub.read_bytes()).verify(sigb, data)
    print("OK: signature valid.")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    ap_k = sub.add_parser("keygen"); ap_k.add_argument("--out", required=True)
    ap_s = sub.add_parser("sign"); ap_s.add_argument("--priv", required=True); ap_s.add_argument("--file", required=True); ap_s.add_argument("--out", required=True)
    ap_v = sub.add_parser("verify"); ap_v.add_argument("--pub", required=True); ap_v.add_argument("--file", required=True); ap_v.add_argument("--sig", required=True)
    args = ap.parse_args()
    if args.cmd == "keygen": keygen(Path(args.out))
    elif args.cmd == "sign": sign(Path(args.priv), Path(args.file), Path(args.out))
    elif args.cmd == "verify": verify(Path(args.pub), Path(args.file), Path(args.sig))

if __name__ == "__main__":
    main()
