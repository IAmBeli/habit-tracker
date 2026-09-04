import pytest
from datetime import date
from django.contrib.auth.models import User
from habits.models import Habit, Completion

@pytest.fixture
def user(db):
    return User.objects.create_user(username="tester", password="pass12345")

@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="other", password="pass12345")

@pytest.fixture
def habit(user):
    return Habit.objects.create(
        user=user,
        title="Gym",
        start_date=date(2020, 1, 1),
        interval_days=1,
    )

@pytest.mark.django_db
def test_today_requires_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/accounts/login/" in response.url

@pytest.mark.django_db
def test_today_shows_own_habits(client, user, habit):
    client.force_login(user)
    response = client.get("/")
    assert response.status_code == 200
    assert habit in [item["habit"] for item in response.context["items"]]

@pytest.mark.django_db
def test_today_hides_other_users_habits(client, other_user, habit):
    client.force_login(other_user)
    response = client.get("/")
    assert response.context["items"] == []

@pytest.mark.django_db
def test_toggle_creates_and_removes_completion(client, user, habit):
    client.force_login(user)

    client.post(f"/habits/{habit.id}/toggle/")
    assert Completion.objects.filter(habit=habit).count() == 1

    client.post(f"/habits/{habit.id}/toggle/")
    assert Completion.objects.filter(habit=habit).count() == 0

@pytest.mark.django_db
def test_cannot_toggle_someone_elses_habit(client, other_user, habit):
    client.force_login(other_user)
    response = client.post(f"/habits/{habit.id}/toggle/")
    assert response.status_code == 404
    assert Completion.objects.count() == 0