from __future__ import annotations
from typing import Dict
from mpmath import iv

def small_interval_checks() -> Dict[str, float | bool]:
    out: Dict[str, float | bool] = {}
    a = iv.mpf([0.999999, 1.000001])
    b = iv.mpf([-1e-12, 1e-12])
    proj = a*b - b + b
    out["interval_demo_contains_zero"] = (proj.a <= 0 <= proj.b)

    dt = iv.mpf([0.0099, 0.0101])
    c  = iv.mpf([0.9,   1.1])
    x0 = iv.mpf([0.99,  1.01])
    x1 = x0 - dt*c*x0
    out["dissipative_step_lower"] = float(x1.a)
    out["dissipative_step_upper"] = float(x1.b)
    return out
