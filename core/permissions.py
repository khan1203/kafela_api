from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsRegularUser(permissions.BasePermission):
    """
    Allows access only to non-admin (regular) users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_staff)

class IsUnauthorizedUser(permissions.BasePermission):
    """
    Allows access only to those users who have not yet registered.
    """

    def has_permission(self, request, view):
        return bool(request.user or request.user.is_staff or not request.user)
