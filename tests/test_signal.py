"""Tests for eaf.signal module."""

from eaf.signal import Signal


class GameObject:

    def __init__(self):

        self.signal = Signal()
        self.fired = 0

    def fire(self):
        self.fired += 1


def test_signal():
    obj1 = GameObject()
    obj2 = GameObject()

    obj1.signal.connect(obj1.fire)

    for obj in (obj1, obj2):
        obj.signal.emit()

    assert obj1.fired == 1
    assert obj2.fired == 0

    # connect second object's method to first object's signal
    obj1.signal.connect(obj2.fire)

    for obj in (obj1, obj2):
        obj.signal.emit()

    assert obj1.fired == 2
    assert obj2.fired == 1
