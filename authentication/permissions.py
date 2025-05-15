from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    """
    Custom permission to make sure that users can only modify their own informations.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user