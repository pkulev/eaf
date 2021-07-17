"""Base handler classes."""

import typing

from abc import ABCMeta, abstractmethod
from typing import (
    Dict,
    Generator,
    List,
    Optional,
)

if typing.TYPE_CHECKING:
    from eaf.state import State


class Handler(metaclass=ABCMeta):
    """Base handler."""

    def __init__(self, owner: State):
        self._owner = owner

    @property
    def owner(self) -> State:
        """Handler's owner getter."""

        return self._owner

    @abstractmethod
    def handle(self):
        """Handle event."""

        raise NotImplementedError  # pragma: no cover


class Event:
    QUIT = "quit"
    SIMPLE = "simple"

    __types__ = {}

    def __init__(self, etype):
        self.type = etype

    def __init_subclass__(cls):
        #self.__types__[cls.__name__]
        return cls

    @classmethod
    def register(cls, etype, eclass):
        cls.__types__[etype] = eclass


class KeyPressedEvent(Event):

    KEYUP = "keyup"
    KEYDOWN = "keydown"

    def __init__(self, up, scancode):
        super().__init__(self, self.KEYUP if up else self.KEYDOWN)
        self._scancode = scancode

    @property
    def scancode(self):
        return self._scancode


class UserEvent(Event):

    USER = "user"

    def __init__(self, data=None):
        super().__init__(self.USER)

        self._data = data

    @property
    def data(self):
        return self._data


class EventQueue:
    """Base event queue."""

    def get(self, event_type=None, pump=True) -> List[Event]:
        raise NotImplementedError

    def post(self, event: Event):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class PygameEventQueue(EventQueue):
    pass


# TODO: remove owner link if it's not needed anymore
class EventHandler(Handler):
    """Base game event handler.

    Handles events using the event queue.
    Provides command mapping manipulations via the default handle() method.
    You must instantiate this class only after application being initialized.
    Application instance has event queue object, that will be used here.

    :param :class:`xoinvader.state.State` owner: handler's owner state
    :param dict command_map: key->command mapping
    """

    def __init__(self, owner: State, event_map: Optional[Dict] = None):
        super().__init__(owner)

        self._event_map = event_map or {}
        # TODO: implement proper queue object
        self._event_queue = owner.app.event_queue

    def on_event(self, event):
        spec = self._event_map.get(event.type)

    def handle(self):
        """Handle incoming events."""

        for event in self._event_queue.get():
            table = self._command_map.get(event.type, {})
            command = table.get(event.
                if callable(command):
                    command()
            else:
                raise ValueError("Unknown event type: {0}".format(event[0]))
