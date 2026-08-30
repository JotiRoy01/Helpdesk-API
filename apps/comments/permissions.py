from rest_framework.permissions import BasePermission

from apps.users.constants import UserRole


class CanAccessTicketComments(BasePermission):
    message = "You do not have permission to access comments for this ticket."

    def has_object_permission(
        self,
        request,
        view,
        ticket,
    ):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.role == UserRole.ADMIN:
            return True

        if user.role == UserRole.CUSTOMER:
            return ticket.creator_id == user.id

        if user.role == UserRole.SUPPORT_AGENT:
            return ticket.assigned_agent_id == user.id

        return False
