from rest_framework.permissions import BasePermission


class IsAuthenticatedTicketUser(BasePermission):
    """
    Base permission for authenticated ticket operations.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )



from rest_framework.permissions import BasePermission

from apps.users.constants import UserRole


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class IsSupportAgentOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {
                UserRole.SUPPORT_AGENT,
                UserRole.ADMIN,
            }
        )


from rest_framework.permissions import BasePermission

from apps.users.constants import UserRole

# Ticket ownership permission
class TicketAccessPermission(BasePermission):
    """
    Controls access to individual tickets.

    Customer:
        Can access own tickets.

    Support Agent:
        Can access tickets assigned to them.

    Admin:
        Can access all tickets.
    """

    message = "You do not have permission to access this ticket."

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.role == UserRole.ADMIN:
            return True

        if user.role == UserRole.CUSTOMER:
            return obj.creator_id == user.id

        if user.role == UserRole.SUPPORT_AGENT:
            return obj.assigned_agent_id == user.id

        return False

# Assignment needs to be restricted to Admin
class CanAssignTicket(BasePermission):
    message = "Only administrators can assign tickets."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


    