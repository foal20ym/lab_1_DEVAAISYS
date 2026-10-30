"""Example API contract tests. Students may add more tests in this file."""
from app import app


def test_valid_prediction():
    """A well-formed request returns one of the supported class labels."""
    client = app.test_client()
    response = client.post(
        "/predict", json={"measurements": [5.1, 3.5, 1.4, 0.2]}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["species"] in {"setosa", "versicolor", "virginica"}


def test_invalid_measurement_count():
    """A request with fewer than four measurements is rejected."""
    client = app.test_client()
    response = client.post("/predict", json={"measurements": [5.1, 3.5]})
    assert response.status_code == 400
    assert "error" in response.get_json()


# Optional ideas for students:
# - The home page (GET /) returns HTTP 200.
# - A missing "measurements" key returns HTTP 400.
# - A nonnumeric measurement returns HTTP 400.
# - A measurement of zero or a very large number returns HTTP 400.

def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_random_page():
    client = app.test_client()
    response = client.get("/should_not_exist")
    assert response.status_code != 200

def test_large_measurement():
    """A request with too large number should be rejected"""
    client = app.test_client()
    response = client.post("/predict", json={"measurements": [9999, 9999]})
    assert response.status_code == 400
    assert "error" in response.get_json()