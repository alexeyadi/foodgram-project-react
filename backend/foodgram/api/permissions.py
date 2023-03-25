from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    '''Check your status. You have access if you are Author or Admin.'''
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Check your status. You have access if you are Admin. Or only read.'''
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)
