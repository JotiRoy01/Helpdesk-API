import pytest

from apps.users.constants import UserRole
from apps.users.models import User
from apps.users.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer_does_not_expose_password():
    user = User.objects.create_user(
        email="security@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    data = UserSerializer(user).data

    assert "password" not in data

# ------------------------
# Token leakage test
# ------------------------
@pytest.mark.django_db
def test_user_response_does_not_include_tokens():
    user = User.objects.create_user(
        email="security2@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    data = UserSerializer(user).data

    serialized = str(data)

    assert "access" not in serialized
    assert "refresh" not in serialized

