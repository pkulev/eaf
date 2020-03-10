import pytest

import eaf.errors

from eaf.app import Application
from eaf.state import State


class MockedApplication(Application):
    @staticmethod
    def _finalize():
        try:
            app = Application.current()
            app.stop()
        except eaf.errors.ApplicationNotInitializedError:
            pass


class MockedState(State):
    pass


@pytest.fixture
def mock_application(request):
    def inner():
        return MockedApplication()

    request.addfinalizer(MockedApplication._finalize)
    return inner


@pytest.fixture
def mock_state(request, mock_application):
    def inner(mock_app=False):
        if mock_app:
            mock_application()
        Application.current().register(MockedState)
        return Application.current().state

    def stop():
        try:
            Application.current().deregister(MockedState.__name__)
        except eaf.errors.ApplicationNotInitializedError:
            pass

    request.addfinalizer(stop)

    return inner
