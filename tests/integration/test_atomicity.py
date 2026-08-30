import pytest

from apps.audit.models import AuditLog
from apps.tickets.services import assign_ticket


@pytest.mark.django_db
def test_assignment_and_audit_are_atomic(
    admin,
    agent,
    ticket,
    monkeypatch,
):
    def fail_audit(**kwargs):
        raise RuntimeError("Simulated audit failure")

    monkeypatch.setattr(
        "apps.tickets.services.audit_ticket_action",
        fail_audit,
    )

    with pytest.raises(RuntimeError):
        assign_ticket(
            ticket=ticket,
            agent=agent,
            actor=admin,
        )

    ticket.refresh_from_db()

    assert ticket.assigned_agent is None

    assert not AuditLog.objects.filter(
        entity_id=ticket.id,
    ).exists()
