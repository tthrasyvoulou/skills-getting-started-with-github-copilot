from urllib.parse import quote


def test_signup_and_unregister_flow(client):
    # Arrange
    email = "tester@example.com"
    activity = "Chess Club"
    a = quote(activity, safe="")
    e = quote(email, safe="")

    # Act: signup
    resp = client.post(f"/activities/{a}/signup?email={e}")
    # Assert: signup succeeded
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # Act: verify it was added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # Act: unregister
    resp = client.delete(f"/activities/{a}/participants?email={e}")
    # Assert: unregister succeeded
    assert resp.status_code == 200
    assert "Unregistered" in resp.json()["message"]

    # Act: verify removal
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "NoSuchActivity"
    email = "someone@example.com"

    # Act
    resp = client.post(f"/activities/{quote(activity, safe='')}/signup?email={quote(email, safe='')}")

    # Assert
    assert resp.status_code == 404


def test_duplicate_signup_returns_400(client):
    # Arrange: use an email already present in baseline data
    existing = "michael@mergington.edu"
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{quote(activity, safe='')}/signup?email={quote(existing, safe='')}")

    # Assert
    assert resp.status_code == 400
