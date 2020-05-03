from eaf.clock import Clock


def test_clock():
    clock = Clock()
    assert isinstance(clock._get_ticks_ms(), int)
    assert isinstance(clock.tick(), int)
    assert isinstance(clock.fps, int)
    assert isinstance(clock.delta, int)
