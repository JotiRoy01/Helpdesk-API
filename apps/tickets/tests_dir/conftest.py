import pytest

from apps.categories.models import Category
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.fixture
def category(db):
    return Category.objects.create(name="Network")


@pytest.fixture
def customer(db):
    return User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )


@pytest.fixture
def another_customer(db):
    return User.objects.create_user(
        email="another@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )