from django.db import models


class TicketPriority(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class TicketStatus(models.TextChoices):
    OPEN = "OPEN", "Open"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    WAITING_FOR_USER = "WAITING_FOR_USER", "Waiting for User"
    RESOLVED = "RESOLVED", "Resolved"
    CLOSED = "CLOSED", "Closed"