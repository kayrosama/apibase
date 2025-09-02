
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEltaOrReadOnly(BasePermission):
    """
    Permite acceso total solo al usuario 'elta'.
    Los demás usuarios solo pueden hacer lecturas (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.username == 'elta'
