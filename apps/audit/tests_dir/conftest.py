import pytest

from apps.categories.models import Category
from apps.tickets.constants import TicketStatus
from apps.tickets.models import Ticket
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
def admin(db):
    return User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        role=UserRole.ADMIN,
    )


@pytest.fixture
def agent(db):
    return User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )


@pytest.fixture
def ticket(db, customer, category):
    return Ticket.objects.create(
        title="VPN issue",
        description="VPN connection is failing.",
        category=category,
        creator=customer,
        status=TicketStatus.OPEN,
    )
