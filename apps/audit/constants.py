from django.db import models


class AuditAction(models.TextChoices):
    TICKET_CREATED = (
        "TICKET_CREATED",
        "Ticket Created",
    )

    TICKET_ASSIGNED = (
        "TICKET_ASSIGNED",
        "Ticket Assigned",
    )

    TICKET_REASSIGNED = (
        "TICKET_REASSIGNED",
        "Ticket Reassigned",
    )

    TICKET_STATUS_CHANGED = (
        "TICKET_STATUS_CHANGED",
        "Ticket Status Changed",
    )

    TICKET_PRIORITY_CHANGED = (
        "TICKET_PRIORITY_CHANGED",
        "Ticket Priority Changed",
    )

    COMMENT_ADDED = (
        "COMMENT_ADDED",
        "Comment Added",
    )

    CATEGORY_CREATED = (
        "CATEGORY_CREATED",
        "Category Created",
    )

    CATEGORY_UPDATED = (
        "CATEGORY_UPDATED",
        "Category Updated",
    )