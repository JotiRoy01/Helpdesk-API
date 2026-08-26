from rest_framework.permissions import BasePermission

from apps.users.constants import UserRole


class IsAuthenticatedUser(BasePermission):
    message = "Authentication is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )


class IsAdmin(BasePermission):
    message = "Administrator access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class IsSupportAgentOrAdmin(BasePermission):
    message = "Support agent or administrator access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {
                UserRole.SUPPORT_AGENT,
                UserRole.ADMIN,
            }
        )


class IsCustomerOrAdmin(BasePermission):
    message = "Customer or administrator access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {
                UserRole.CUSTOMER,
                UserRole.ADMIN,
            }
        )