import uuid

import pytest
from rest_framework.test import APIClient

from apps.tickets.models import Ticket
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_ticket_not_found_returns_safe_response():
    user = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(
        f"/api/v1/tickets/{uuid.uuid4()}/",
    )

    assert response.status_code == 404
    assert response.data["success"] is False
    assert (
        response.data["code"]
        == "TICKET_NOT_FOUND"
    )



@pytest.mark.django_db
def test_private_ticket_does_not_leak_as_forbidden(
    customer,
    another_customer,
    category,
):
    ticket = Ticket.objects.create(
        title="Private ticket",
        description="Private issue description.",
        category=category,
        creator=customer,
    )

    client = APIClient()
    client.force_authenticate(
        user=another_customer,
    )

    response = client.get(
        f"/api/v1/tickets/{ticket.id}/",
    )

    assert response.status_code == 404

    assert (
        response.data["code"]
        == "TICKET_NOT_FOUND"
    )

