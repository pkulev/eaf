"""EAF core things."""

from __future__ import annotations

from typing import Type


class Vec3(object):
    """3D vector representation."""

    __slots__ = ("x", "y", "z")

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return "Vec3(x={0}, y={1}, z={2})".format(self.x, self.y, self.z)

    __str__ = __repr__

    @staticmethod
    def _value_error(operation, value):
        """Raise ValueError with appropriate message."""

        return ValueError(
            "Wrong type to {0} {1}: {2}".format(operation, type(value), value)
        )

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(x=self.x + other, y=self.y + other, z=self.z + other)

        elif isinstance(other, Vec3):
            return Vec3(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)
        else:
            raise self._value_error("add", other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.__add__(-other)
        elif isinstance(other, Vec3):
            return Vec3(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)
        else:
            raise self._value_error("sub", other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(x=self.x * other, y=self.y * other, z=self.z * other)
        else:
            raise self._value_error("mul", other)

    # FIXME: it's quite unusual to divide vectors
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vec3(x=self.x / other, y=self.y / other, z=self.z / other)
        else:
            raise self._value_error("div", other)

    __div__ = __truediv__

    def __eq__(self, other):
        if not isinstance(other, Vec3):
            raise self._value_error("eq", other)

        return self.x == other.x and self.y == other.y and self.z == other.z

    def __getitem__(self, cons: Type) -> Vec3:
        """Cast vector items to selected type."""

        return Vec3(x=cons(self.x), y=cons(self.y), z=cons(self.z))

    def as_tuple2(self) -> tuple:
        """Return x and y as tuple."""

        return (self.x, self.y)

    def as_tuple3(self) -> tuple:

        return (self.x, self.y, self.z)

    as_tuple = as_tuple3
