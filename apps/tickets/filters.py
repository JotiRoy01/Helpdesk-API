import django_filters

from django.db import models
from django.utils import timezone

from .constants import TicketPriority, TicketStatus
from .models import Ticket


class TicketFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=TicketStatus.choices,
    )

    priority = django_filters.ChoiceFilter(
        field_name="priority",
        choices=TicketPriority.choices,
    )

    category = django_filters.UUIDFilter(
        field_name="category_id",
    )

    assigned_agent = django_filters.UUIDFilter(
        field_name="assigned_agent_id",
    )

    creator = django_filters.UUIDFilter(
        field_name="creator_id",
    )

    is_overdue = django_filters.BooleanFilter(
        method="filter_overdue",
    )

    class Meta:
        model = Ticket

        fields = (
            "status",
            "priority",
            "category",
            "assigned_agent",
            "creator",
            "is_overdue",
        )

    def filter_overdue(
        self,
        queryset,
        name,
        value,
    ):
        if value is True:
            return queryset.filter(
                due_at__lt=timezone.now(),
            ).exclude(
                status__in=[
                    TicketStatus.RESOLVED,
                    TicketStatus.CLOSED,
                ]
            )

        if value is False:
            return queryset.filter(
                models.Q(due_at__gte=timezone.now())
                | models.Q(due_at__isnull=True)
                | models.Q(
                    status__in=[
                        TicketStatus.RESOLVED,
                        TicketStatus.CLOSED,
                    ]
                )
            )

        return queryset