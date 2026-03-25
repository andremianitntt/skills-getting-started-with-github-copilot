import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory database before each test"""
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        }
    })


def test_get_activities():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    # Arrange
    email = "andre.cavalcanti@nttdata.com"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "andre.cavalcanti@nttdata.com"
    client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400


def test_signup_activity_not_found():
    # Arrange
    email = "andre.cavalcanti@nttdata.com"

    # Act
    response = client.post(
        "/activities/Unknown/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404


def test_delete_participant_success():
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_delete_participant_not_found():
    # Arrange
    email = "notfound@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404


def test_delete_activity_not_found():
    # Arrange
    email = "andre.cavalcanti@nttdata.com"

    # Act
    response = client.delete(
        "/activities/Unknown/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404