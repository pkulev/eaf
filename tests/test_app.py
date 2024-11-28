"""Unittests for eaf.app module."""

import pytest

import eaf.app
import eaf.errors
from eaf.app import Application

from .common import AnotherStateMock, StateMock


def test_empty_application():
    assert pytest.raises(eaf.errors.ApplicationNotInitializedError, eaf.app.current)
    assert pytest.raises(eaf.errors.ApplicationNotInitializedError, Application.current)

    app = Application()
    assert eaf.app.current() is app
    assert Application.current() is app

    assert pytest.raises(eaf.errors.ApplicationIsEmpty, lambda app=app: app.state)
    assert pytest.raises(eaf.errors.ApplicationIsEmpty, app.start)

    assert app.renderer is not None
    assert app.event_queue is None

    assert app.fps is not None
    app.fps = 40
    assert app.fps == 40

    assert eaf.app.current() is app
    del app
    assert pytest.raises(eaf.errors.ApplicationNotInitializedError, eaf.app.current)


def test_single_state_application():
    app = Application()
    app.register(StateMock)

    assert len(app._states) == 1  # pylint: disable=protected-access
    assert isinstance(app.state, StateMock)

    assert pytest.raises(
        eaf.errors.ApplicationStateIsNotRegistered,
        lambda: setattr(app, "state", "test"),
    )


def test_multiple_state_application(monkeypatch):
    app = Application()
    app.register(StateMock)
    app.register(AnotherStateMock)

    assert len(app.states) == 2
    # Ensure that Application._state hasn't changed
    assert isinstance(app.state, StateMock)

    app.state = AnotherStateMock.__name__
    assert isinstance(app.state, AnotherStateMock)

    # Test Application.trigger_state
    called_with = []

    def new_trigger(self, *args, **kwargs):
        called_with.extend([args, kwargs])

    monkeypatch.setattr(StateMock, "trigger", new_trigger)
    app.trigger_state(StateMock.__name__, 10, test=20)
    assert isinstance(app.state, StateMock)
    assert called_with == [(10,), {"test": 20}]

    # Test Application.trigger_reinit
    app.state.marker = "something"
    assert hasattr(app.state, "marker") is True
    app.trigger_reinit(StateMock.__name__)
    assert isinstance(app.state, StateMock)
    assert hasattr(app.state, "marker") is False

    assert pytest.raises(ValueError, lambda: setattr(app, "fps", "thirty"))


def test_application_loop():
    app = Application()
    app.register(StateMock)
    # FIXME: test loop properly
    # assert app.start() is None

    app.register(AnotherStateMock)
    app.state = AnotherStateMock.__name__
    # FIXME: test loop properly
    # assert app.start() is None
    assert app.stop() is None
