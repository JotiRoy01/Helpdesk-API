import pytest

from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.tickets.models import Ticket
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_customer_can_comment_on_own_ticket():
    customer = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    category = Category.objects.create(
        name="Network",
    )

    ticket = Ticket.objects.create(
        title="VPN issue",
        description="VPN connection is failing.",
        category=category,
        creator=customer,
    )

    client = APIClient()
    client.force_authenticate(
        user=customer,
    )

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments/",
        {
            "message": "Additional information.",
        },
        format="json",
    )

    assert response.status_code == 201


# -------------------------------------
# Test another customer cannot comment
# -------------------------------------

@pytest.mark.django_db
def test_customer_cannot_comment_on_other_customer_ticket():
    owner = User.objects.create_user(
        email="owner@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    another_customer = User.objects.create_user(
        email="another@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    category = Category.objects.create(
        name="Network",
    )

    ticket = Ticket.objects.create(
        title="Private ticket",
        description="Private customer issue.",
        category=category,
        creator=owner,
    )

    client = APIClient()
    client.force_authenticate(
        user=another_customer,
    )

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments/",
        {
            "message": "I should not be able to write here.",
        },
        format="json",
    )

    assert response.status_code == 404

# ----------------------------------
# Test assigned agent comment
# ----------------------------------

@pytest.mark.django_db
def test_assigned_agent_can_comment():
    customer = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    agent = User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    category = Category.objects.create(
        name="Network",
    )

    ticket = Ticket.objects.create(
        title="VPN issue",
        description="VPN connection is failing.",
        category=category,
        creator=customer,
        assigned_agent=agent,
    )

    client = APIClient()
    client.force_authenticate(
        user=agent,
    )

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments/",
        {
            "message": "I am investigating this issue.",
        },
        format="json",
    )

    assert response.status_code == 201


# -------------------------------------------
# Test unassigned agent
# -------------------------------------------
@pytest.mark.django_db
def test_unassigned_agent_cannot_comment():
    customer = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    assigned_agent = User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    another_agent = User.objects.create_user(
        email="agent2@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    category = Category.objects.create(
        name="Network",
    )

    ticket = Ticket.objects.create(
        title="VPN issue",
        description="VPN connection is failing.",
        category=category,
        creator=customer,
        assigned_agent=assigned_agent,
    )

    client = APIClient()
    client.force_authenticate(
        user=another_agent,
    )

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments/",
        {
            "message": "I should not be here.",
        },
        format="json",
    )

    assert response.status_code == 404

# -------------------------------------
# Test admin comment
# -------------------------------------
@pytest.mark.django_db
def test_admin_can_comment_on_any_ticket():
    customer = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    admin = User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        role=UserRole.ADMIN,
    )

    category = Category.objects.create(
        name="Network",
    )

    ticket = Ticket.objects.create(
        title="VPN issue",
        description="VPN connection is failing.",
        category=category,
        creator=customer,
    )

    client = APIClient()
    client.force_authenticate(
        user=admin,
    )

    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments/",
        {
            "message": "Administrative review completed.",
        },
        format="json",
    )

    assert response.status_code == 201

