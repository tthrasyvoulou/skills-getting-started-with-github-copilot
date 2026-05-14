import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

# Capture baseline activities to restore between tests
_ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: restore baseline before the test runs
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
    yield
    # Teardown: ensure baseline restored after test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))


@pytest.fixture
def client():
    # Provide a TestClient instance for tests
    with TestClient(app_module.app) as c:
        yield c
