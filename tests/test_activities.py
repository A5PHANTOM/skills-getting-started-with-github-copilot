def test_get_activities_returns_expected_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload

    chess = payload["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_signup_success_adds_participant(client):
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/Chess Club/signup?email={email}")

    assert response.status_code == 200
    assert "Successfully signed up" in response.json()["message"]

    activities_response = client.get("/activities")
    assert email in activities_response.json()["Chess Club"]["participants"]


def test_signup_activity_not_found_returns_404(client):
    response = client.post("/activities/Unknown Club/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_full_activity_returns_400(client):
    # Tennis Club starts with 1 participant and max of 10; add 9 to fill it.
    for index in range(9):
        client.post(f"/activities/Tennis Club/signup?email=student{index}@mergington.edu")

    response = client.post("/activities/Tennis Club/signup?email=overflow@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unregister_success_removes_participant(client):
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/Chess Club/participants?email={email}")

    assert response.status_code == 200
    assert "Successfully unregistered" in response.json()["message"]

    activities_response = client.get("/activities")
    assert email not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_activity_not_found_returns_404(client):
    response = client.delete("/activities/Unknown Club/participants?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    response = client.delete("/activities/Chess Club/participants?email=notenrolled@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant is not signed up for this activity"


def test_signup_then_unregister_lifecycle(client):
    email = "lifecycle@mergington.edu"

    signup_response = client.post(f"/activities/Robotics Club/signup?email={email}")
    assert signup_response.status_code == 200

    after_signup = client.get("/activities")
    assert email in after_signup.json()["Robotics Club"]["participants"]

    unregister_response = client.delete(f"/activities/Robotics Club/participants?email={email}")
    assert unregister_response.status_code == 200

    after_unregister = client.get("/activities")
    assert email not in after_unregister.json()["Robotics Club"]["participants"]
