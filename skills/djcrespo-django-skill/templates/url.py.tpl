from django.urls import path, include
from rest_framework.routers import DefaultRouter

from {{ app_name }}.views import {{ model_name }}ViewSet


router = DefaultRouter()
router.register(r"{{ url_basename }}", {{ model_name }}ViewSet, basename="{{ url_basename }}")

urlpatterns = [
    path("", include(router.urls)),
]
