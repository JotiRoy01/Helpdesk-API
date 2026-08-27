from django.db.models import Count, Q
from django.utils import timezone

from apps.tickets.constants import TicketStatus
from apps.users.constants import UserRole
from apps.tickets.models import Ticket
from apps.users.models import User
from apps.tickets.overdue import ACTIVE_STATUSES
from django.db.models import Count




def get_ticket_summary():
    now = timezone.now()

    return Ticket.objects.aggregate(
        total=Count("id"),

        open=Count(
            "id",
            filter=Q(
                status=TicketStatus.OPEN,
            ),
        ),

        in_progress=Count(
            "id",
            filter=Q(
                status=TicketStatus.IN_PROGRESS,
            ),
        ),

        waiting_for_user=Count(
            "id",
            filter=Q(
                status=TicketStatus.WAITING_FOR_USER,
            ),
        ),

        resolved=Count(
            "id",
            filter=Q(
                status=TicketStatus.RESOLVED,
            ),
        ),

        closed=Count(
            "id",
            filter=Q(
                status=TicketStatus.CLOSED,
            ),
        ),

        overdue=Count(
            "id",
            filter=Q(
                due_at__lt=now,
                status__in={
                    TicketStatus.OPEN,
                    TicketStatus.IN_PROGRESS,
                    TicketStatus.WAITING_FOR_USER,
                },
            ),
        ),
    )

# -------------------------------------------------
# workload should include useful metrics
# -------------------------------------------------
def get_agent_workload():
    return (
        User.objects
        .filter(
            role=UserRole.SUPPORT_AGENT,
            is_active=True,
        )
        .annotate(
            assigned_ticket_count=Count(
                "assigned_tickets",
            ),

            open_count=Count(
                "assigned_tickets",
                filter=Q(
                    assigned_tickets__status=TicketStatus.OPEN,
                ),
            ),

            in_progress_count=Count(
                "assigned_tickets",
                filter=Q(
                    assigned_tickets__status=(
                        TicketStatus.IN_PROGRESS
                    ),
                ),
            ),

            waiting_for_user_count=Count(
                "assigned_tickets",
                filter=Q(
                    assigned_tickets__status=(
                        TicketStatus.WAITING_FOR_USER
                    ),
                ),
            ),

            overdue_count=Count(
                "assigned_tickets",
                filter=Q(
                    assigned_tickets__due_at__lt=timezone.now(),
                    assigned_tickets__status__in=(
                        ACTIVE_STATUSES
                    ),
                ),
            ),
        )
        .values(
            "id",
            "email",
            "first_name",
            "last_name",
            "assigned_ticket_count",
            "open_count",
            "in_progress_count",
            "waiting_for_user_count",
            "overdue_count",
        )
        .order_by(
            "-assigned_ticket_count",
            "first_name",
        )
    )

# -------------------------------------------
# Create user-scoped summary selector
# -------------------------------------------

def get_agent_summary(*, agent):
    now = timezone.now()

    return Ticket.objects.filter(
        assigned_agent=agent,
    ).aggregate(
        total=Count("id"),

        open=Count(
            "id",
            filter=Q(
                status=TicketStatus.OPEN,
            ),
        ),

        in_progress=Count(
            "id",
            filter=Q(
                status=TicketStatus.IN_PROGRESS,
            ),
        ),

        waiting_for_user=Count(
            "id",
            filter=Q(
                status=TicketStatus.WAITING_FOR_USER,
            ),
        ),

        resolved=Count(
            "id",
            filter=Q(
                status=TicketStatus.RESOLVED,
            ),
        ),

        closed=Count(
            "id",
            filter=Q(
                status=TicketStatus.CLOSED,
            ),
        ),

        overdue=Count(
            "id",
            filter=Q(
                due_at__lt=now,
                status__in=ACTIVE_STATUSES,
            ),
        ),
    )