#!/usr/bin/env bash
set -euo pipefail
BROOT="bundles"
VZIP="$BROOT/ValorAIPlus_Global_Proof_Package_vFinal.zip"
RZIP="$BROOT/ValorAIPlus_Global_Proof_Package_Rebuilt.zip"

[ -f "$VZIP" ] && echo "[OK] found $VZIP" || { echo "[ERR] missing $VZIP"; exit 2; }
[ -f "$RZIP" ] && echo "[OK] found $RZIP" || { echo "[ERR] missing $RZIP"; exit 2; }

# optional SHA receipts at repo root
if [ -f "SHA_RECEIPTS.txt" ]; then
  if command -v sha256sum >/dev/null 2>&1; then H="sha256sum"; else H="shasum -a 256"; fi
  for z in "$VZIP" "$RZIP"; do
    got=$($H "$z" | awk '{print $1}')
    expected=$(grep -F "  $(basename "$z")" SHA_RECEIPTS.txt | awk '{print $1}' || true)
    [ -n "$expected" ] && [ "$got" != "$expected" ] && { echo "[FAIL] SHA mismatch for $z"; exit 4; }
    [ -n "$expected" ] && echo "[OK] SHA matches for $(basename "$z")"
  done
else
  echo "[WARN] SHA_RECEIPTS.txt not found; skipping ZIP hash verification"
fi

mkdir -p "$BROOT/vFinal" "$BROOT/Rebuilt"
unzip -o "$VZIP" -d "$BROOT/vFinal"   >/dev/null
unzip -o "$RZIP" -d "$BROOT/Rebuilt" >/dev/null
echo "[DONE] Unpacked to:"
echo " - $BROOT/vFinal"
echo " - $BROOT/Rebuilt"
