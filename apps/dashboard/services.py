from .selectors import (
    get_agent_summary,
    get_agent_workload,
    get_ticket_summary,
)


def get_dashboard_summary():
    return get_ticket_summary()


def get_dashboard_workload():
    return list(get_agent_workload())


def get_summary_for_user(*, user):
    from apps.users.constants import UserRole

    if user.role == UserRole.ADMIN:
        return get_ticket_summary()

    return get_agent_summary(
        agent=user,
    )
