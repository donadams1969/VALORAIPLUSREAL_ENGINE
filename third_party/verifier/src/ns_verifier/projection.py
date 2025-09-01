from __future__ import annotations
from typing import Dict, Tuple
from .backends import ArrayModule
from .fftwrap import rfftn3, irfftn3
from .grid import wave_numbers

def divergence(xp: ArrayModule, ux, uy, uz):
    Ux = rfftn3(xp, ux); Uy = rfftn3(xp, uy); Uz = rfftn3(xp, uz)
    nx, ny, nz = ux.shape
    KX, KY, KZ, _ = wave_numbers(xp, nx, ny, nz)
    div_hat = 1j*(KX*Ux + KY*Uy + KZ*Uz)
    return irfftn3(xp, div_hat, (nx,ny,nz))

def project(xp: ArrayModule, ux, uy, uz, dt: float):
    nx, ny, nz = ux.shape
    Ux = rfftn3(xp, ux); Uy = rfftn3(xp, uy); Uz = rfftn3(xp, uz)
    KX, KY, KZ, K2 = wave_numbers(xp, nx, ny, nz)
    div_hat = 1j*(KX*Ux + KY*Uy + KZ*Uz)
    with xp.errstate(divide='ignore', invalid='ignore'):
        p_hat = -div_hat/(dt*K2)
        p_hat = xp.where(K2==0, 0.0, p_hat)
    px_hat = 1j*KX*p_hat; py_hat = 1j*KY*p_hat; pz_hat = 1j*KZ*p_hat
    ux_new = ux - dt*irfftn3(xp, px_hat, (nx,ny,nz))
    uy_new = uy - dt*irfftn3(xp, py_hat, (nx,ny,nz))
    uz_new = uz - dt*irfftn3(xp, pz_hat, (nx,ny,nz))
    return ux_new, uy_new, uz_new, p_hat

def l2_norm_per_cell(xp: ArrayModule, a) -> float:
    n = 1
    for s in a.shape: n *= s
    return float(xp.linalg.norm(a)/n)

def projection_check(xp: ArrayModule, nx: int, ny: int, nz: int, dt: float = 1e-2) -> Dict[str, float]:
    from .grid import linspace_box
    X, Y, Z = linspace_box(xp, nx, ny, nz)
    ux = xp.sin(X)*xp.cos(Y)*xp.cos(Z)
    uy = -xp.cos(X)*xp.sin(Y)*xp.cos(Z)
    uz = 0.1*xp.sin(X+Y+Z)

    div_before = divergence(xp, ux, uy, uz)
    ux2, uy2, uz2, _ = project(xp, ux, uy, uz, dt)
    div_after = divergence(xp, ux2, uy2, uz2)

    return {
        "div_before_l2_per_cell": l2_norm_per_cell(xp, div_before),
        "div_after_l2_per_cell": l2_norm_per_cell(xp, div_after)
    }
