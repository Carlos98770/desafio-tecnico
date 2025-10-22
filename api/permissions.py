from rest_framework.permissions import BasePermission
from django.conf import settings

class HasAPIKey(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get("Authorization")
        if not api_key:
            return False
        return api_key == f"Api-Key {settings.API_KEY}"
