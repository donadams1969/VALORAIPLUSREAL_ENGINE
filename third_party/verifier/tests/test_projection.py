import numpy as np
from ns_verifier.backends import get_xp
from ns_verifier.projection import projection_check

def test_projection_reduces_divergence():
    xp = get_xp(False)  # CPU path
    m = projection_check(xp, 16, 16, 16, dt=1e-2)
    assert m["div_after_l2_per_cell"] < m["div_before_l2_per_cell"]
    assert m["div_after_l2_per_cell"] < 1e-6  # loose sanity bound for tiny grid
