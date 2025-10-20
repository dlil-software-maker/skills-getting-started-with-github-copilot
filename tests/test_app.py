from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # ensure some known activity exists
    assert "Chess Club" in data


def test_signup_and_reflect():
    activity = "Test Class"
    email = "test_user@example.com"

    # make sure activity exists in in-memory activities for this test
    activities[activity] = {
        "description": "A test activity",
        "schedule": "Now",
        "max_participants": 5,
        "participants": []
    }

    # sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # fetch activities and ensure participant present
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    data = resp2.json()
    assert email in data[activity]["participants"]


def test_unregister_participant():
    activity = "Test Class"
    email = "remove_me@example.com"

    # ensure participant present
    activities.setdefault(activity, {
        "description": "A test activity",
        "schedule": "Now",
        "max_participants": 5,
        "participants": []
    })
    activities[activity]["participants"].append(email)

    # remove
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "Unregistered" in body.get("message", "")

    # verify removed
    assert email not in activities[activity]["participants"]
