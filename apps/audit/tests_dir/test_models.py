import pytest

from apps.audit.constants import AuditAction
from apps.audit.models import AuditLog
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_audit_log_creation():
    user = User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        role=UserRole.ADMIN,
    )

    log = AuditLog.objects.create(
        actor=user,
        action=AuditAction.TICKET_CREATED,
        entity_type="Ticket",
        entity_id=__import__("uuid").uuid4(),
        new_value={
            "status": "OPEN",
        },
    )

    assert log.actor == user
    assert log.action == AuditAction.TICKET_CREATED
