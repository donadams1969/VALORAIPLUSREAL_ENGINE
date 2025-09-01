from __future__ import annotations
from typing import Protocol, Any

try:
    import cupy as cp  # type: ignore
except Exception:  # pragma: no cover
    cp = None

import numpy as np

class ArrayModule(Protocol):
    def array(self, *a: Any, **k: Any): ...
    fft: Any
    linalg: Any
    def meshgrid(self, *args: Any, **kwargs: Any): ...
    def linspace(self, *args: Any, **kwargs: Any): ...
    def where(self, *args: Any, **kwargs: Any): ...
    def errstate(self, *args: Any, **kwargs: Any):
        class Dummy:
            def __enter__(self): return None
            def __exit__(self, *a): return False
        return Dummy()

def get_xp(use_gpu: bool) -> ArrayModule:
    if use_gpu and cp is not None:
        return cp  # type: ignore
    return np  # type: ignore

def is_gpu(xp: ArrayModule) -> bool:
    return (cp is not None) and (xp is cp)  # type: ignore
