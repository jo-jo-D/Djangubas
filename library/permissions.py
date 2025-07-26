from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsOwnerOrReadOnly(BasePermission):
    """
    Кастомное разрешение, которое позволяет редактировать объект
    только его владельцу. Остальным доступно только чтение.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение (GET, HEAD, OPTIONS) даем всем.
        # SAFE_METHODS - это кортеж ('GET', 'HEAD', 'OPTIONS').
        if request.method in SAFE_METHODS:
            return True
        # Разрешения на запись (POST, PUT, PATCH, DELETE) даем только владельцу объекта.
        return obj.owner == request.user
