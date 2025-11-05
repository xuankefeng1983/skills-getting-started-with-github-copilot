from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity_name = "Chess Club"
    test_email = "pytest.user@example.com"

    # Ensure clean state
    if test_email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(test_email)

    # Signup
    resp = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant present via GET
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    participants = resp2.json()[activity_name]["participants"]
    assert test_email in participants

    # Delete (unregister)
    resp3 = client.delete(f"/activities/{activity_name}/participants?email={test_email}")
    assert resp3.status_code == 200
    assert "Removed" in resp3.json().get("message", "")

    # Final check
    resp4 = client.get("/activities")
    assert resp4.status_code == 200
    participants_final = resp4.json()[activity_name]["participants"]
    assert test_email not in participants_final
