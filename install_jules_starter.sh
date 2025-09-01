#!/usr/bin/env bash
set -euo pipefail

# ===========================
# VALOR / JULES STARTER INSTALLER (v2.1)
# ===========================
# What it does:
#  - Creates ./bundles and ./modules (if missing)
#  - If SHA_RECEIPTS.txt exists, verifies SHA-256 for known files
#  - Copies (or refreshes) the two core bundles into ./bundles
#  - Optionally copies the modular starter into ./modules
#
# Expected filenames (exact) placed NEXT TO THIS SCRIPT:
#   1) ValorAIPlus_Global_Proof_Package_vFinal.zip
#   2) ValorAIPlus_Global_Proof_Package_Rebuilt.zip
#   3) VALORAIPLUS2E_Modular_Starter_v1.zip   (optional)
#
# Usage:
#   bash install_jules_starter.sh .
#
# Optional:
#   Place a SHA_RECEIPTS.txt next to this script to enforce hashes.
#   Format per line: "<sha256>  <filename>"

DEST_ROOT="${1:-.}"
VFINAL="ValorAIPlus_Global_Proof_Package_vFinal.zip"
REBUILT="ValorAIPlus_Global_Proof_Package_Rebuilt.zip"
STARTER="VALORAIPLUS2E_Modular_Starter_v1.zip"   # optional
SHA_FILE="SHA_RECEIPTS.txt"

mkdir -p "$DEST_ROOT/bundles" "$DEST_ROOT/modules"

# --- hasher selection
if command -v sha256sum >/dev/null 2>&1; then
  HASHER="sha256sum"
elif command -v shasum >/dev/null 2>&1; then
  HASHER="shasum -a 256"
else
  echo "[ERROR] Need sha256sum or shasum installed." >&2
  exit 3
fi

check_present () {
  local f="$1"
  if [ -f "$f" ]; then
    echo "[FOUND] $f"
    return 0
  else
    echo "[MISSING] $f"
    return 1
  fi
}

verify_sha () {
  local f="$1"
  if [ ! -f "$SHA_FILE" ]; then
    echo "[WARN] $SHA_FILE not found; skipping SHA check for $f"
    return 0
  fi
  local expected
  expected=$(grep -F "  $f" "$SHA_FILE" | awk '{print $1}' || true)
  if [ -z "$expected" ]; then
    echo "[WARN] No SHA line for $f in $SHA_FILE; skipping check"
    return 0
  fi
  local got
  got=$($HASHER "$f" | awk '{print $1}')
  if [ "$expected" != "$got" ]; then
    echo "[FAIL] SHA mismatch for $f" >&2
    echo " expected: $expected" >&2
    echo "      got: $got" >&2
    exit 4
  fi
  echo "[OK] SHA-256 matches for $f"
}

copied=0

# ---- vFinal
if check_present "$VFINAL"; then
  verify_sha "$VFINAL"
  cp -f "$VFINAL" "$DEST_ROOT/bundles/$VFINAL"
  echo "[COPY] $VFINAL -> $DEST_ROOT/bundles/"
  copied=$((copied+1))
fi

# ---- Rebuilt
if check_present "$REBUILT"; then
  verify_sha "$REBUILT"
  cp -f "$REBUILT" "$DEST_ROOT/bundles/$REBUILT"
  echo "[COPY] $REBUILT -> $DEST_ROOT/bundles/"
  copied=$((copied+1))
fi

# ---- Optional starter
if check_present "$STARTER"; then
  verify_sha "$STARTER" || true
  cp -f "$STARTER" "$DEST_ROOT/modules/$STARTER"
  echo "[COPY] $STARTER -> $DEST_ROOT/modules/"
fi

echo "[DONE] Copied $copied bundle(s) into $DEST_ROOT/bundles."
if [ "$copied" -eq 0 ]; then
  cat <<'EONOTE'
[NOTE] I did not find the required zips next to this script.
       Please upload these files into the SAME folder as this script, then rerun:

  - ValorAIPlus_Global_Proof_Package_vFinal.zip
  - ValorAIPlus_Global_Proof_Package_Rebuilt.zip
  (optional: VALORAIPLUS2E_Modular_Starter_v1.zip)

If you have a SHA_RECEIPTS.txt, place it next to this script to enable verification.
EONOTE
fi
