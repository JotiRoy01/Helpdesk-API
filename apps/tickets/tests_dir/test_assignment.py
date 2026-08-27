import pytest

from django.core.exceptions import ValidationError

from apps.categories.models import Category
from apps.tickets.constants import TicketStatus
from apps.tickets.models import Ticket
from apps.tickets.services import assign_ticket
from apps.users.constants import UserRole
from apps.users.models import User
from rest_framework.test import APIClient

# ------------------------
# fixtures
# ------------------------
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
def agent(db):
    return User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )


@pytest.fixture
def inactive_agent(db):
    return User.objects.create_user(
        email="inactive@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
        is_active=False,
    )


@pytest.fixture
def admin(db):
    return User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        role=UserRole.ADMIN,
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

# ------------------
# Test successful assigment
# ------------------
@pytest.mark.django_db
def test_admin_can_assign_ticket(
    admin,
    agent,
    ticket,
):
    updated_ticket = assign_ticket(
        ticket=ticket,
        agent=agent,
        actor=admin,
    )

    updated_ticket.refresh_from_db()

    assert updated_ticket.assigned_agent == agent

# -----------------------------
# Test customer cannot assign
# -----------------------------
@pytest.mark.django_db
def test_customer_cannot_assign_ticket(
    customer,
    agent,
    ticket,
):
    with pytest.raises(ValidationError):
        assign_ticket(
            ticket=ticket,
            agent=agent,
            actor=customer,
        )

# --------------------------
# Test agent cannot assign
# --------------------------
@pytest.mark.django_db
def test_agent_cannot_assign_ticket(
    agent,
    ticket,
):
    another_agent = User.objects.create_user(
        email="agent2@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    with pytest.raises(ValidationError):
        assign_ticket(
            ticket=ticket,
            agent=another_agent,
            actor=agent,
        )

# ----------------------------
# Test invalid target role
# ----------------------------
@pytest.mark.django_db
def test_admin_cannot_assign_customer(
    admin,
    customer,
    ticket,
):
    with pytest.raises(ValidationError):
        assign_ticket(
            ticket=ticket,
            agent=customer,
            actor=admin,
        )

# --------------------------------
# Test inactive agent
# --------------------------------
@pytest.mark.django_db
def test_admin_cannot_assign_inactive_agent(
    admin,
    inactive_agent,
    ticket,
):
    with pytest.raises(ValidationError):
        assign_ticket(
            ticket=ticket,
            agent=inactive_agent,
            actor=admin,
        )

# ------------------------------------
# Test reassignment
# ------------------------------------
@pytest.mark.django_db
def test_admin_can_reassign_ticket(
    admin,
    agent,
    ticket,
):
    second_agent = User.objects.create_user(
        email="agent2@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    assign_ticket(
        ticket=ticket,
        agent=agent,
        actor=admin,
    )

    assign_ticket(
        ticket=ticket,
        agent=second_agent,
        actor=admin,
    )

    ticket.refresh_from_db()

    assert ticket.assigned_agent == second_agent


# ------------------------------------
# API authorization tests
# ------------------------------------
@pytest.mark.django_db
def test_customer_cannot_use_assignment_endpoint(
    customer,
    agent,
    ticket,
):
    client = APIClient()

    client.force_authenticate(
        user=customer,
    )

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/assign/",
        {
            "assigned_agent": str(agent.id),
        },
        format="json",
    )

    assert response.status_code == 403


# -------------------------------
# Test Admin API assignment
# -------------------------------
@pytest.mark.django_db
def test_admin_can_use_assignment_endpoint(
    admin,
    agent,
    ticket,
):
    client = APIClient()

    client.force_authenticate(
        user=admin,
    )

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/assign/",
        {
            "assigned_agent": str(agent.id),
        },
        format="json",
    )

    assert response.status_code == 200

    ticket.refresh_from_db()

    assert ticket.assigned_agent == agent

# ---------------------------------
# Test inactive agent at API level
# ---------------------------------
@pytest.mark.django_db
def test_admin_cannot_assign_inactive_agent_through_api(
    admin,
    inactive_agent,
    ticket,
):
    client = APIClient()

    client.force_authenticate(
        user=admin,
    )

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/assign/",
        {
            "assigned_agent": str(
                inactive_agent.id
            ),
        },
        format="json",
    )

    assert response.status_code == 400

