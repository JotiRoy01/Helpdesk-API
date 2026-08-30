import uuid

import pytest

from apps.audit.constants import AuditAction
from apps.audit.models import AuditLog
from apps.audit.services import create_audit_log
from apps.users.constants import UserRole
from apps.users.models import User


@pytest.mark.django_db
def test_create_audit_log():
    user = User.objects.create_user(
        email="admin@example.com",
        password="StrongPassword123!",
        role=UserRole.ADMIN,
    )

    entity_id = uuid.uuid4()

    log = create_audit_log(
        actor=user,
        action=AuditAction.TICKET_CREATED,
        entity_type="Ticket",
        entity_id=entity_id,
        new_value={
            "status": "OPEN",
        },
    )

    assert log.id is not None
    assert log.actor == user
    assert log.entity_id == entity_id
    assert log.new_value == {
        "status": "OPEN",
    }

    assert AuditLog.objects.count() == 1
