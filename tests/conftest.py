from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """Provide a FastAPI test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activity state for isolated tests."""
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
