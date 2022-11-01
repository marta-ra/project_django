from candy.services import CategoryServices
from unittest.mock import MagicMock, patch
from django.test import SimpleTestCase


class CandyServicesTestCase(SimpleTestCase):

    @patch('candy.services.category_services.Category')
    def test_get_categories(self, category_model_patch):

        categories_mock = MagicMock()
        category_model_patch.objects.all.return_value = categories_mock

        result = CategoryServices.get_categories()

        self.assertEqual(result, categories_mock)
        category_model_patch.objects.all.assert_called_once_with()

    @patch('candy.services.category_services.Category')
    def test_get_category(self, category_model_patch):

        category_mock = MagicMock()
        category_id_mock = MagicMock()
        category_model_patch.objects.get.return_value = category_mock

        result = CategoryServices.get_category(category_id_mock)

        self.assertEqual(result, category_mock)
        category_model_patch.objects.get.assert_called_once_with(pk=category_id_mock)
