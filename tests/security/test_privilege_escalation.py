import pytest

from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_registration_cannot_create_admin(
    api_client,
):
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
