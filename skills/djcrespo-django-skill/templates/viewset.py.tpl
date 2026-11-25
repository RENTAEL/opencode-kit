from rest_framework import viewsets

from {{ app_name }}.models import {{ model_name }}
from {{ app_name }}.serializers import (
    {{ model_name }}ReadSerializer,
    {{ model_name }}WriteSerializer,
)


class {{ model_name }}ViewSet(viewsets.ModelViewSet):
    """ViewSet for {{ model_name }}."""

    queryset = {{ model_name }}.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return {{ model_name }}WriteSerializer
        return {{ model_name }}ReadSerializer
