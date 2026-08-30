import pytest
from rest_framework.test import APIClient

from apps.users.constants import UserRole
from apps.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_creates_customer(api_client):
    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "email": "customer@example.com",
            "first_name": "John",
            "last_name": "Customer",
            "password": "StrongPassword123!",
            "password_confirmation": "StrongPassword123!",
        },
        format="json",
    )

    assert response.status_code == 201

    user = User.objects.get(
        email="customer@example.com",
    )

    assert user.role == UserRole.CUSTOMER


@pytest.mark.django_db
def test_registration_cannot_create_admin(api_client):
    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "email": "attacker@example.com",
            "first_name": "Attacker",
            "last_name": "User",
            "password": "StrongPassword123!",
            "password_confirmation": "StrongPassword123!",
            "role": UserRole.ADMIN,
        },
        format="json",
    )

    assert response.status_code == 201

    user = User.objects.get(
        email="attacker@example.com",
    )

    assert user.role == UserRole.CUSTOMER


# login test
@pytest.mark.django_db
def test_login_returns_tokens(api_client):
    User.objects.create_user(
        email="login@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "email": "login@example.com",
            "password": "StrongPassword123!",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data["data"]["tokens"]
    assert "refresh" in response.data["data"]["tokens"]


# wrong password test
@pytest.mark.django_db
def test_invalid_login_is_rejected(api_client):
    User.objects.create_user(
        email="login@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "email": "login@example.com",
            "password": "WrongPassword123!",
        },
        format="json",
    )

    assert response.status_code == 400


# protected end point test
@pytest.mark.django_db
def test_me_requires_authentication(api_client):
    response = api_client.get(
        "/api/v1/auth/me/",
    )

    assert response.status_code == 401


# then authentication


@pytest.mark.django_db
def test_me_returns_authenticated_user(api_client):
    user = User.objects.create_user(
        email="me@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "email": "me@example.com",
            "password": "StrongPassword123!",
        },
        format="json",
    )

    access_token = response.data["data"]["tokens"]["access"]

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = api_client.get(
        "/api/v1/auth/me/",
    )

    assert response.status_code == 200
    assert response.data["data"]["id"] == str(user.id)
