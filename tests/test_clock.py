import math
import time

from eaf.clock import Clock


def test_clock():
    clock = Clock()
    t1 = int(time.monotonic())

    assert clock.delta == 0
    assert clock.fps == 0

    dt = clock.tick()
    t2 = int(time.monotonic())

    assert math.isclose(t2 - t1, dt)
    assert clock.delta == dt
