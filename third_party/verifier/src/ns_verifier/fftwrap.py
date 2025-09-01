from __future__ import annotations
from typing import Tuple
from .backends import ArrayModule

def rfftn3(xp: ArrayModule, a):
    return xp.fft.rfftn(a, axes=(0,1,2))

def irfftn3(xp: ArrayModule, A, shape: Tuple[int,int,int]):
    return xp.fft.irfftn(A, s=shape, axes=(0,1,2))
