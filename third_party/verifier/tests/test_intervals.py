from ns_verifier.intervals import small_interval_checks

def test_interval_contains_zero():
    out = small_interval_checks()
    assert out["interval_demo_contains_zero"] is True
