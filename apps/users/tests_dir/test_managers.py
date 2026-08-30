import pytest

from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_create_user_hashes_password():
    user = User.objects.create_user(
        email="user@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    assert user.password != "StrongPassword123!"
    assert user.check_password("StrongPassword123!")


@pytest.mark.django_db
def test_superuser_is_admin():
    user = User.objects.create_superuser(
        email="admin@example.com",
        password="StrongPassword123!",
    )

    assert user.role == UserRole.ADMIN
    assert user.is_staff is True
    assert user.is_superuser is True
