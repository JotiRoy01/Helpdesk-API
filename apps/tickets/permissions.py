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