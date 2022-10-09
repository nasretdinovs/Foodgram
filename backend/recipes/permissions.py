from rest_framework import permissions


class AuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Доступ автору, остальным только чтение."""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET',)
            or (request.user == obj.author)
            or request.user.is_staff
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Доступ администратору, остальным только чтение."""
    def has_permission(self, request, view):
        return (
            request.method in ('GET',)
            or request.user.is_authenticated
            and request.user.is_admin
        )


class OwnerUserOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Доступ администратору и автору, остальным только чтение."""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET',)
            or (request.user == obj)
            or request.user.is_admin
        )


class OwnerUser(permissions.IsAuthenticated):
    """Доступ только автору."""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET',)
            or (request.user == obj)
            or request.user.is_admin
        )
