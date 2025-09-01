from __future__ import annotations
from typing import Tuple
from .backends import ArrayModule

def wave_numbers(xp: ArrayModule, nx: int, ny: int, nz: int):
    kx = xp.fft.fftfreq(nx) * nx
    ky = xp.fft.fftfreq(ny) * ny
    kz = xp.fft.rfftfreq(nz) * nz
    KX, KY, KZ = xp.meshgrid(kx, ky, kz, indexing='ij')
    K2 = KX*KX + KY*KY + KZ*KZ
    return KX, KY, KZ, K2

def linspace_box(xp: ArrayModule, nx: int, ny: int, nz: int, L: float = 6.283185307179586):
    x = xp.linspace(0, L, nx, endpoint=False)
    y = xp.linspace(0, L, ny, endpoint=False)
    z = xp.linspace(0, L, nz, endpoint=False)
    return xp.meshgrid(x, y, z, indexing='ij')
