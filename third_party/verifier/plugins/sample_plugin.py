"""
Sample plugin. Place this file in a directory and set:
  export NS_VERIFIER_PLUGIN_PATH=/abs/path/to/that/dir
Then run:
  nsverify plugins
"""
from typing import Dict, Any

def register(registry: Dict[str, Any]) -> None:
    def demo():
        # A trivial plugin that returns a constant metric
        return {"hello": "from plugin", "ok": True}
    registry["sample_plugin"] = demo
