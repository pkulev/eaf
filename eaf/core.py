"""EAF core things."""

from __future__ import annotations

from typing import Any


class Vec3:
    """3D vector representation."""

    __slots__ = ("x", "y", "z")

    def __init__(self, x: int | float = 0, y: int | float = 0, z: int | float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Vec3(x={self.x}, y={self.y}, z={self.z})"

    __str__ = __repr__

    @staticmethod
    def _value_error(operation: str, value: Any) -> ValueError:
        """Raise ValueError with appropriate message."""

        return ValueError(f"Wrong type to {operation} {type(value)}: {value}")

    def __add__(self, other: object) -> Vec3:
        if isinstance(other, int | float):
            return Vec3(x=self.x + other, y=self.y + other, z=self.z + other)

        elif isinstance(other, Vec3):
            return Vec3(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)
        else:
            raise self._value_error("add", other)

    def __sub__(self, other: object) -> Vec3:
        if isinstance(other, int | float):
            return self.__add__(-other)
        elif isinstance(other, Vec3):
            return Vec3(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)
        else:
            raise self._value_error("sub", other)

    def __mul__(self, other: object) -> Vec3:
        if isinstance(other, int | float):
            return Vec3(x=self.x * other, y=self.y * other, z=self.z * other)
        else:
            raise self._value_error("mul", other)

    # FIXME: it's quite unusual to divide vectors
    def __truediv__(self, other: object) -> Vec3:
        if isinstance(other, int | float):
            return Vec3(x=self.x / other, y=self.y / other, z=self.z / other)
        else:
            raise self._value_error("div", other)

    __div__ = __truediv__

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec3):
            raise self._value_error("eq", other)

        return self.x == other.x and self.y == other.y and self.z == other.z

    def __getitem__(self, cons: type) -> Vec3:
        """Cast vector items to selected type."""

        return Vec3(x=cons(self.x), y=cons(self.y), z=cons(self.z))

    def as_tuple2(self) -> tuple[int | float, int | float]:
        """Return x and y as tuple."""

        return (self.x, self.y)

    def as_tuple3(self) -> tuple[int | float, int | float, int | float]:
        return (self.x, self.y, self.z)

    as_tuple = as_tuple3
