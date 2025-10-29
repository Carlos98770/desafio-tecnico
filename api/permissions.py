from rest_framework.permissions import BasePermission
from django.conf import settings

class HasAPIKey(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return False
            
        try:
            scheme, api_key = auth_header.split()
        except ValueError:
            # Falha se não houver um espaço (ex: "Api-KeyMinhaChave")
            return False

        # Compara de forma segura (ignorando maiúsculas/minúsculas no scheme)
        # e comparando a chave com a sua API_KEY
        return scheme.lower() == "api-key" and api_key == settings.API_KEY