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