"""Useful metaclasses."""


class Singleton(type):
    """Singleton metaclass."""

    _instances: dict[type, object] = {}

    def __call__(cls, *args, **kwds) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwds)
        return cls._instances[cls]
