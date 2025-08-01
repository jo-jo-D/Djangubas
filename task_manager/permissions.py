from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser or request.user.is_staff

    def has_object_permission(self, obj, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user