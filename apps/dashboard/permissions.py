from rest_framework.permissions import BasePermission

from apps.users.constants import UserRole


class CanViewDashboard(BasePermission):
    message = "You do not have permission to access the dashboard."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.role in {
            UserRole.ADMIN,
            UserRole.SUPPORT_AGENT,
        }

# -------------------------------------------
# workload endpoint should remain admin-only
# -------------------------------------------
class IsAdminDashboard(BasePermission):
    message = "Administrator access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )
