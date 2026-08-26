from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.users.constants import UserRole


class IsAdminOrReadOnly(BasePermission):
    """
    Allow public reads for the categories API.
    Only admins can create, update, or delete categories.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role == UserRole.ADMIN