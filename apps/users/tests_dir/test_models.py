import pytest

from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_user_email_is_unique():
    User.objects.create_user(
        email="test@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    with pytest.raises(Exception):
        User.objects.create_user(
            email="test@example.com",
            password="AnotherPassword123!",
            role=UserRole.CUSTOMER,
        )


@pytest.mark.django_db
def test_customer_role():
    user = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    assert user.is_customer is True
    assert user.is_support_agent is False
    assert user.is_admin is False