import pytest
from rest_framework.test import APIClient

from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_customer_cannot_view_audit_logs():
    customer = User.objects.create_user(
        email="customer@example.com",
        password="StrongPassword123!",
        role=UserRole.CUSTOMER,
    )

    client = APIClient()
    client.force_authenticate(user=customer)

    response = client.get("/api/v1/audit-logs/")

    assert response.status_code == 403


# --------------
# Agent
# --------------
@pytest.mark.django_db
def test_agent_cannot_view_audit_logs():
    agent = User.objects.create_user(
        email="agent@example.com",
        password="StrongPassword123!",
        role=UserRole.SUPPORT_AGENT,
    )

    client = APIClient()
    client.force_authenticate(user=agent)

    response = client.get("/api/v1/audit-logs/")

    assert response.status_code == 403


# -----------------------
# Admin
# -----------------------
@pytest.mark.django_db
def test_admin_can_view_audit_logs():
    admin = User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        role=UserRole.ADMIN,
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.get("/api/v1/audit-logs/")

    assert response.status_code == 200
