from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    """
    Allow access to only staff users
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.is_active
