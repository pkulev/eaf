import pytest

from eaf.core import Vec3
from eaf.obj import Object


def test_object():
    obj = Object()
    assert obj.pos == Vec3(0, 0, 0)
    obj.pos = Vec3(1, 1, 1)
    assert obj.pos == Vec3(1, 1, 1)

    with pytest.raises(NotImplementedError):
        obj.update(0)

    assert obj.type == "Object"

    assert Object(Vec3(1, 0, 0)).pos == Vec3(1, 0, 0)
