from apps.audit.constants import AuditAction
from apps.audit.models import AuditLog
from apps.comments.models import Comment
from apps.tickets.constants import TicketPriority, TicketStatus


def test_complete_ticket_lifecycle(
    api_client,
    customer,
    admin,
    agent,
    category,
):
    # Customer authentication
    login_response = api_client.post(
        "/api/v1/auth/login/",
        {
            "email": customer.email,
            "password": "StrongPassword123!",
        },
        format="json",
    )

    assert login_response.status_code == 200

    access_token = (
        login_response.data["data"]["tokens"]["access"]
    )

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    # Create ticket
    create_response = api_client.post(
        "/api/v1/tickets/",
        {
            "title": "VPN connection issue",
            "description": (
                "Unable to connect to the "
                "office VPN."
            ),
            "category": str(category.id),
            "priority": TicketPriority.HIGH,
        },
        format="json",
    )

    assert create_response.status_code == 201

    ticket_id = create_response.data["data"]["id"]

    # Admin assigns agent
    api_client.force_authenticate(
        user=admin,
    )

    assign_response = api_client.post(
        f"/api/v1/tickets/{ticket_id}/assign/",
        {
            "assigned_agent": str(agent.id),
        },
        format="json",
    )

    assert assign_response.status_code == 200

    # Agent authenticates
    api_client.force_authenticate(
        user=agent,
    )

    # Transition to in progress
    transition_response = api_client.post(
        f"/api/v1/tickets/{ticket_id}/transition/",
        {
            "status": TicketStatus.IN_PROGRESS,
        },
        format="json",
    )

    assert transition_response.status_code == 200

    # Agent comments
    comment_response = api_client.post(
        f"/api/v1/tickets/{ticket_id}/comments/",
        {
            "message": (
                "I am investigating "
                "the VPN issue."
            ),
        },
        format="json",
    )

    assert comment_response.status_code == 201

    # Resolve
    transition_response = api_client.post(
        f"/api/v1/tickets/{ticket_id}/transition/",
        {
            "status": TicketStatus.RESOLVED,
        },
        format="json",
    )

    assert transition_response.status_code == 200

    # Admin closes
    api_client.force_authenticate(
        user=admin,
    )

    transition_response = api_client.post(
        f"/api/v1/tickets/{ticket_id}/transition/",
        {
            "status": TicketStatus.CLOSED,
        },
        format="json",
    )

    assert transition_response.status_code == 200

    # Verify comment
    assert Comment.objects.filter(
        ticket_id=ticket_id,
    ).exists()

    # Verify audit trail
    actions = set(
        AuditLog.objects.filter(
            entity_id=ticket_id,
        ).values_list(
            "action",
            flat=True,
        )
    )

    assert AuditAction.TICKET_CREATED in actions
    assert AuditAction.TICKET_ASSIGNED in actions
    assert AuditAction.TICKET_STATUS_CHANGED in actions
    assert AuditAction.COMMENT_ADDED in actions