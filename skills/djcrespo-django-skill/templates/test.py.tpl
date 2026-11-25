from django.test import TestCase

from {{ app_name }}.models import {{ model_name }}


class {{ model_name }}Tests(TestCase):
    def test_create_{{ model_snake }}(self):
        instance = {{ model_name }}.objects.create()
        self.assertIsNotNone(instance.id)
        self.assertTrue(instance.is_active)

    def test_list_{{ model_plural }}(self):
        {{ model_name }}.objects.create()
        self.assertEqual({{ model_name }}.objects.count(), 1)

    def test_soft_delete_{{ model_snake }}(self):
        instance = {{ model_name }}.objects.create()
        instance.is_active = False
        instance.save()
        self.assertFalse({{ model_name }}.objects.filter(is_active=True).exists())
