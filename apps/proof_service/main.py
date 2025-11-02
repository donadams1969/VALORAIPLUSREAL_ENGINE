from fastapi import FastAPI, Response
from pathlib import Path
import os, json, hashlib, unicodedata

app = FastAPI(title="valoraiplus_ V0 Proof Service (C3PA0)")

DATA = Path("data")
LICENSE = DATA/"VALOR_Doctrinal_License_v1.44g_canonical.txt"
MANIFEST = DATA/"VDL_v1.44g_manifest.json"

# fallbacks from env to keep branding consistent
VP_MOD  = os.getenv("valoraiplus_module_id","VALORAIPLUS_V0_PROOF_v1.44g")
VP_GILL = os.getenv("valoraiplus_GILLBTC","VALORCHAIN-G::GHOST25")
VP_TXID = os.getenv("valoraiplus_btc_txid","00"*32)

def canon(text:str)->str:
    t = unicodedata.normalize("NFC", text).replace("\r\n","\n").replace("\r","\n")
    lines = [ln.rstrip() for ln in t.split("\n")]
    t = "\n".join(lines)
    if not t.endswith("\n"): t += "\n"
    return t

@app.get("/health")
def health(): return {"ok":True, "brand":"valoraiplus_", "module":VP_MOD}

@app.get("/manifest")
def manifest():
    if MANIFEST.exists():
        m = json.loads(MANIFEST.read_text())
        # guarantee anchors in response even if file was external
        m.setdefault("valoraiplus_module_id", VP_MOD)
        m.setdefault("valoraiplus_GILLBTC", VP_GILL)
        m.setdefault("valoraiplus_btc_txid", VP_TXID)
        m.setdefault("valoraiplus_brand", "valoraiplus_")
        return m
    return {"error":"manifest not found","valoraiplus_module_id":VP_MOD}

@app.get("/hashcheck")
def hashcheck():
    c = canon(LICENSE.read_text(encoding="utf-8")).encode()
    return {
      "sha3_512": hashlib.sha3_512(c).hexdigest().upper(),
      "sha256": hashlib.sha256(c).hexdigest(),
      "valoraiplus_module_id": VP_MOD,
      "valoraiplus_GILLBTC": VP_GILL,
      "valoraiplus_btc_txid": VP_TXID
    }

@app.get("/badge")
def badge():
    return {
      "title":"VALOR Doctrinal License v1.44g",
      "badge":"valoraiplus_: Anchor truth • Whistleblower protected • Trauma-informed validators • 7B fork ≥4/12 • E-SIGN recognized",
      "holder":"DG77.77X-Ξ",
      "valoraiplus_module_id": VP_MOD,
      "valoraiplus_GILLBTC": VP_GILL,
      "valoraiplus_btc_txid": VP_TXID
    }

@app.get("/opreturn.hex")
def opreturn_hex():
    man = json.loads(MANIFEST.read_text())
    return Response(man["op_return"]+"\n", media_type="text/plain")

@app.get("/op25.hex")
def op25_hex():
    man = json.loads(MANIFEST.read_text())
    return Response(man["op25_return"]+"\n", media_type="text/plain")
