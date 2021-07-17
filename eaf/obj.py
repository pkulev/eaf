import uuid
from typing import Optional

from eaf.core import Vec3
from eaf.node import Node


class Object(Node):
    """Object representation.

    Object supports hierarchy via it's superclass Node.
    Objects live within some state.
    You can place invisible objects anywhere for things like controllers and
    managers.
    """

    default_name_template = "Object"

    def __init__(self, pos: Optional[Vec3] = None):
        super().__init__()

        if pos is None:
            pos = Vec3(0, 0, 0)

        self._pos = pos
        self._id = uuid.uuid4()

    @property
    def id(self):
        """Object uinique identifier."""

        return self._id

    @property
    def type(self) -> str:
        """Type getter for registration purposes."""

        return self.__class__.__name__

    @property
    def pos(self) -> Vec3:
        """Object's position getter."""

        return self._pos

    @pos.setter
    def pos(self, pos: Vec3):
        """Object's position setter."""

        self._pos = pos

    def update(self, dt: int):
        """Update object, called every frame by the state."""

        raise NotImplementedError
