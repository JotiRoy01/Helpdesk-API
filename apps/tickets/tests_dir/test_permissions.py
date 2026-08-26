import pytest

from apps.categories.models import Category
from apps.tickets.models import Ticket
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Network",
    )


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


@pytest.fixture
def agent(db):
    return User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )


@pytest.fixture
def another_agent(db):
    return User.objects.create_user(
        email="agent2@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )


@pytest.fixture
def admin(db):
    return User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        role=UserRole.ADMIN,
    )


@pytest.fixture
def customer_ticket(customer, category):
    return Ticket.objects.create(
        title="Customer ticket",
        description="Customer issue description.",
        category=category,
        creator=customer,
    )

# Test customer ownership
@pytest.mark.django_db
def test_customer_can_access_own_ticket(
    customer,
    customer_ticket,
):
    assert (
        customer_ticket.creator_id
        == customer.id
    )

# API-level test is
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_customer_sees_only_own_tickets(
    customer,
    another_customer,
    category,
):
    Ticket.objects.create(
        title="Own ticket",
        description="This belongs to customer.",
        category=category,
        creator=customer,
    )

    Ticket.objects.create(
        title="Other ticket",
        description="This belongs elsewhere.",
        category=category,
        creator=another_customer,
    )

    client = APIClient()

    response = client.post(
        "/api/v1/auth/login/",
        {
            "email": "customer@example.com",
            "password": "StrongPassword123!",
        },
        format="json",
    )

    access_token = (
        response.data["data"]["tokens"]["access"]
    )

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    response = client.get(
        "/api/v1/tickets/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1

# test agent visibility

@pytest.mark.django_db
def test_agent_sees_only_assigned_tickets(
    agent,
    another_agent,
    customer,
    category,
):
    Ticket.objects.create(
        title="Assigned ticket",
        description="Assigned to current agent.",
        category=category,
        creator=customer,
        assigned_agent=agent,
    )

    Ticket.objects.create(
        title="Other assigned ticket",
        description="Assigned to another agent.",
        category=category,
        creator=customer,
        assigned_agent=another_agent,
    )

    client = APIClient()

    response = client.post(
        "/api/v1/auth/login/",
        {
            "email": "agent@example.com",
            "password": "StrongPassword123!",
        },
        format="json",
    )

    access_token = (
        response.data["data"]["tokens"]["access"]
    )

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    response = client.get(
        "/api/v1/tickets/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1

# test admin visibility
@pytest.mark.django_db
def test_admin_sees_all_tickets(
    admin,
    customer,
    category,
):
    Ticket.objects.create(
        title="Ticket One",
        description="First ticket description.",
        category=category,
        creator=customer,
    )

    Ticket.objects.create(
        title="Ticket Two",
        description="Second ticket description.",
        category=category,
        creator=customer,
    )

    client = APIClient()

    response = client.post(
        "/api/v1/auth/login/",
        {
            "email": "admin@example.com",
            "password": "StrongPassword123!",
        },
        format="json",
    )

    access_token = (
        response.data["data"]["tokens"]["access"]
    )

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    response = client.get(
        "/api/v1/tickets/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 2

# test agent cannot manage another agent's ticket
@pytest.mark.django_db
def test_agent_cannot_transition_unassigned_ticket(
    another_agent,
    customer,
    category,
):
    ticket = Ticket.objects.create(
        title="Another agent ticket",
        description="Ticket belongs to another agent.",
        category=category,
        creator=customer,
        assigned_agent=another_agent,
        status="IN_PROGRESS",
    )

    with pytest.raises(Exception):
        TicketWorkflow.transition(
            ticket=ticket,
            new_status=TicketStatus.RESOLVED,
            actor=agent,
        )

# test customer cannot access another customer's ticket
@pytest.mark.django_db
def test_customer_cannot_access_another_customer_ticket(
    customer,
    another_customer,
    category,
):
    other_ticket = Ticket.objects.create(
        title="Private ticket",
        description="Another customer's issue.",
        category=category,
        creator=another_customer,
    )

    client = APIClient()

    response = client.post(
        "/api/v1/auth/login/",
        {
            "email": "customer@example.com",
            "password": "StrongPassword123!",
        },
        format="json",
    )

    access_token = (
        response.data["data"]["tokens"]["access"]
    )

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    response = client.get(
        f"/api/v1/tickets/{other_ticket.id}/"
    )

    assert response.status_code == 404

# test unauthorized access
@pytest.mark.django_db
def test_unauthenticated_user_cannot_list_tickets():
    client = APIClient()

    response = client.get(
        "/api/v1/tickets/"
    )

    assert response.status_code == 401

    