# ------------------------------------------
# Add comment authorization tests
# ------------------------------------------
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
        title="VPN issue",
        description="VPN connection is failing.",
        category=category,
        creator=customer,
    )

# ------------------------------------------
# Customer can access own ticket comments
# ------------------------------------------
from apps.comments.permissions import (
    CanAccessTicketComments,
)


from unittest.mock import Mock


@pytest.mark.django_db
def test_customer_can_access_own_ticket_comments(
    customer,
    customer_ticket,
):
    request = Mock()
    request.user = customer

    permission = CanAccessTicketComments()

    assert permission.has_object_permission(
        request,
        None,
        customer_ticket,
    ) is True

# --------------------------------
# Another customer must be denied
# --------------------------------
@pytest.mark.django_db
def test_customer_cannot_access_other_customer_comments(
    another_customer,
    customer_ticket,
):
    request = Mock()
    request.user = another_customer

    permission = CanAccessTicketComments()

    assert permission.has_object_permission(
        request,
        None,
        customer_ticket,
    ) is False


# -------------------------------------------
# Assigned agent can access comments
# -------------------------------------------
@pytest.mark.django_db
def test_assigned_agent_can_access_comments(
    agent,
    customer,
    category,
):
    ticket = Ticket.objects.create(
        title="VPN issue",
        description="VPN connection is failing.",
        category=category,
        creator=customer,
        assigned_agent=agent,
    )

    request = Mock()
    request.user = agent

    permission = CanAccessTicketComments()

    assert permission.has_object_permission(
        request,
        None,
        ticket,
    ) is True

# --------------------------------------------
# Another agent must be denied
# --------------------------------------------

@pytest.mark.django_db
def test_other_agent_cannot_access_comments(
    agent,
    another_agent,
    customer,
    category,
):
    ticket = Ticket.objects.create(
        title="VPN issue",
        description="VPN connection is failing.",
        category=category,
        creator=customer,
        assigned_agent=agent,
    )

    request = Mock()
    request.user = another_agent

    permission = CanAccessTicketComments()

    assert permission.has_object_permission(
        request,
        None,
        ticket,
    ) is False


# -----------------------------------------
# Admin can access all comments
# -----------------------------------------
@pytest.mark.django_db
def test_admin_can_access_any_comments(
    admin,
    customer_ticket,
):
    request = Mock()
    request.user = admin

    permission = CanAccessTicketComments()

    assert permission.has_object_permission(
        request,
        None,
        customer_ticket,
    ) is True

