import pytest
from audio import mastering_limiter as mod

CASES = [
    ("look", 'm.lookahead_samples(5, 48000) == 240'),
    ("tpeak", 'm.true_peak(0.9, 1.1) == approx(0.99)'),
    ("attack", 'm.attack_samples(1, 48000) == 48'),
    ("release", 'm.release_samples(10, 48000) == 480'),
    ("link", 'm.stereo_link_gain(2, 1, 1) == approx(0.5)'),
    ("lat", 'm.latency_compensation(48, 48000) == approx(0.001)'),
    ("float", 'm.float_preserve(32) is True'),
    ("dither", 'm.dither_last("final") is True'),
    ("downmix", 'm.downmix_center(3, 1, 1) == approx(2.0)'),
    ("reset", 'm.reset_filter(True) is True'),
    ("os", 'm.oversample_factor(2) == 4'),
    ("gainred", 'm.gain_reduction(-1, 0) == approx(-1.0)'),
    ("apply", 'm.apply_gain(1, 0) == approx(1.0)'),
    ("ceil", 'm.limiter_ceiling(2, 1) == approx(1.0)'),
    ("block", 'm.block_key(10, 4) == 2')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
