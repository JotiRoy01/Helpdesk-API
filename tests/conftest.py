import pytest

from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def customer(db):
    return User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        first_name="Test",
        last_name="Customer",
        role=UserRole.CUSTOMER,
    )


@pytest.fixture
def another_customer(db):
    return User.objects.create_user(
        email="customer2@example.com",
        password="StrongPassword123!",
        first_name="Another",
        last_name="Customer",
        role=UserRole.CUSTOMER,
    )


@pytest.fixture
def agent(db):
    return User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        first_name="Test",
        last_name="Agent",
        role=UserRole.SUPPORT_AGENT,
    )


@pytest.fixture
def another_agent(db):
    return User.objects.create_user(
        email="agent2@example.com",
        password="StrongPassword123!",
        first_name="Another",
        last_name="Agent",
        role=UserRole.SUPPORT_AGENT,
    )


@pytest.fixture
def admin(db):
    return User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        first_name="Test",
        last_name="Admin",
        role=UserRole.ADMIN,
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Network",
        description="Network-related issues.",
    )


@pytest.fixture
def authenticated_customer(api_client, customer):
    api_client.force_authenticate(user=customer)
    return api_client


@pytest.fixture
def authenticated_agent(api_client, agent):
    api_client.force_authenticate(user=agent)
    return api_client


@pytest.fixture
def authenticated_admin(api_client, admin):
    api_client.force_authenticate(user=admin)
    return api_client


# ---------------------------------------
# Create a ticket fixture
# ---------------------------------------
from apps.tickets.constants import TicketPriority, TicketStatus
from apps.tickets.models import Ticket


@pytest.fixture
def customer_ticket(customer, category):
    return Ticket.objects.create(
        title="VPN connection issue",
        description="Unable to connect to the office VPN.",
        category=category,
        priority=TicketPriority.HIGH,
        status=TicketStatus.OPEN,
        creator=customer,
    )


@pytest.fixture
def ticket(customer_ticket):
    return customer_ticket


@pytest.fixture
def assigned_ticket(customer, agent, category):
    return Ticket.objects.create(
        title="Assigned network issue",
        description="Network connectivity is unstable.",
        category=category,
        priority=TicketPriority.HIGH,
        status=TicketStatus.OPEN,
        creator=customer,
        assigned_agent=agent,
    )

