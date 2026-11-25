from rest_framework import serializers

from {{ app_name }}.models import {{ model_name }}


class {{ model_name }}WriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = {{ model_name }}
        fields = [{{ fields_serializer }}]


class {{ model_name }}ReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = {{ model_name }}
        fields = [{{ fields_serializer }}]
        read_only_fields = [{{ fields_serializer }}]
