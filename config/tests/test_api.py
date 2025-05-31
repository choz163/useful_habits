import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='user1', password='pass1')

@pytest.fixture
def user_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def other_user():
    return User.objects.create_user(username='user2', password='pass2')

@pytest.fixture
def other_client(api_client, other_user):
    api_client.force_authenticate(user=other_user)
    return api_client

@pytest.fixture
def habit(user):
    return Habit.objects.create(
        user=user,
        place='home',
        time='12:00:00',
        action='read',
        periodicity=1,
        duration=60,
        is_public=False
    )

@pytest.fixture
def public_habit(other_user):
    return Habit.objects.create(
        user=other_user,
        place='office',
        time='09:00:00',
        action='run',
        periodicity=2,
        duration=30,
        is_public=True
    )

@pytest.mark.django_db
def test_my_list_requires_auth(api_client):
    url = reverse('my-habits')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_my_list_returns_only_own_habits(user_client, user, other_user):
    h1 = Habit.objects.create(
        user=user, place='p', time='10:00:00', action='a', periodicity=1, duration=10
    )
    Habit.objects.create(
        user=other_user, place='p', time='11:00:00', action='b', periodicity=1, duration=10
    )
    url = reverse('my-habits')
    resp = user_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert 'results' in data
    assert len(data['results']) == 1
    assert data['results'][0]['id'] == h1.id

@pytest.mark.django_db
def test_my_list_pagination(user_client, user):
    for i in range(6):
        Habit.objects.create(
            user=user, place=str(i), time='08:00:00', action='act', periodicity=1, duration=10
        )
    url = reverse('my-habits') + '?page=2'
    resp = user_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data['count'] == 6
    assert data['next'] is None
    assert data['previous'] is not None
    assert len(data['results']) == 1

@pytest.mark.django_db
def test_create_habit(user_client, user):
    url = reverse('my-habits')
    payload = {
        'place': 'work',
        'time': '07:30:00',
        'action': 'meditate',
        'periodicity': 3,
        'duration': 45,
        'is_public': True
    }
    resp = user_client.post(url, payload, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert data['place'] == 'work'
    assert data['user'] == user.id
    assert Habit.objects.filter(id=data['id'], user=user).exists()

@pytest.mark.django_db
def test_retrieve_habit_owner(user_client, habit):
    url = reverse('habit-detail', args=[habit.id])
    resp = user_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data['id'] == habit.id
    assert data['action'] == habit.action

@pytest.mark.django_db
def test_retrieve_habit_not_owner_not_public(other_client, habit):
    url = reverse('habit-detail', args=[habit.id])
    resp = other_client.get(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_retrieve_habit_public(other_client, public_habit):
    url = reverse('habit-detail', args=[public_habit.id])
    resp = other_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_habit_owner(user_client, habit):
    url = reverse('habit-detail', args=[habit.id])
    resp = user_client.patch(url, {'action': 'write'}, format='json')
    assert resp.status_code == status.HTTP_200_OK
    habit.refresh_from_db()
    assert habit.action == 'write'

@pytest.mark.django_db
def test_update_habit_not_owner(other_client, habit):
    url = reverse('habit-detail', args=[habit.id])
    resp = other_client.patch(url, {'action': 'hack'}, format='json')
    assert resp.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_delete_habit_owner(user_client, habit):
    url = reverse('habit-detail', args=[habit.id])
    resp = user_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert not Habit.objects.filter(id=habit.id).exists()

@pytest.mark.django_db
def test_delete_habit_not_owner(other_client, habit):
    url = reverse('habit-detail', args=[habit.id])
    resp = other_client.delete(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_public_list_anyone(api_client, user, public_habit, habit):
    url = reverse('public-habits')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    ids = {item['id'] for item in data['results']}
    assert public_habit.id in ids
    assert habit.id not in ids

@pytest.mark.django_db
def test_public_list_pagination(api_client, other_user):
    for i in range(7):
        Habit.objects.create(
            user=other_user, place=str(i), time='06:00:00',
            action='act', periodicity=1, duration=10, is_public=True
        )
    url = reverse('public-habits') + '?page=2'
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data['count'] == 7
    assert len(data['results']) == 2
