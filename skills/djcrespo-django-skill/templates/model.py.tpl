import uuid

from django.db import models


class {{ model_name }}(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    {{ fields_model }}

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "{{ model_name }}"
        verbose_name_plural = "{{ model_name }}s"
        db_table = "{{ model_plural }}"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.id)
