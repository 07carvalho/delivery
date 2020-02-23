from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow only super users
    to edit or delete a partner.
    """

    def has_object_permission(self, request, view, obj):
        print(permissions.SAFE_METHODS)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

