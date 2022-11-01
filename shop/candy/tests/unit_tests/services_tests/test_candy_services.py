from candy.services import CandyServices
from unittest.mock import MagicMock, patch, call
from django.test import SimpleTestCase


class CandyServicesTestCase(SimpleTestCase):

    @patch('candy.services.candy_services.CandyAmount')
    def test_create_candy_amount(self, candy_amount_model_patch):

        order_mock = MagicMock()
        candy_mock = MagicMock()
        quantity_mock = MagicMock()
        candy_amount_mock = MagicMock()
        candy_amount_model_patch.objects.create.return_value = candy_amount_mock

        result = CandyServices.create_candy_amount(order_mock, candy_mock, quantity_mock)

        self.assertEqual(result, candy_amount_mock)
        candy_amount_model_patch.objects.create.assert_called_once_with(order=order_mock, candy=candy_mock,
                                                                        quantity=quantity_mock)

    def test_get_candies_by_category(self):

        category_mock = MagicMock()
        candies_mock = MagicMock()
        category_mock.candies.all.return_value = candies_mock

        result = CandyServices.get_candies_by_category(category_mock)

        self.assertEqual(result, candies_mock)
        category_mock.candies.all.assert_called_once_with()

    @patch('candy.services.candy_services.Candy')
    def test_get_candy(self, candy_model_patch):

        candy_id_mock = MagicMock()
        candy_mock = MagicMock()
        candy_model_patch.objects.get.return_value = candy_mock

        result = CandyServices.get_candy(candy_id_mock)

        self.assertEqual(result, candy_mock)
        candy_model_patch.objects.get.assert_called_once_with(pk=candy_id_mock)

    @patch('candy.services.candy_services.CandyAmount')
    def test_get_candy_amount(self, candy_amount_model_patch):

        candy_amount_id_mock = MagicMock()
        amount_mock = MagicMock()
        candy_amount_model_patch.objects.get.return_value = amount_mock

        result = CandyServices.get_candy_amount(candy_amount_id_mock)

        self.assertEqual(result, amount_mock)
        candy_amount_model_patch.objects.get.assert_called_once_with(pk=candy_amount_id_mock)

    @patch('candy.services.candy_services.Sum')
    @patch('candy.services.candy_services.F')
    def test_get_sum_order(self, f_patch, sum_patch):

        order_candies_with_price_mock = MagicMock()
        total_price_mock = MagicMock()
        order_candies_with_price_mock.aggregate.return_value = total_price_mock

        result = CandyServices.get_sum_order(order_candies_with_price_mock)

        order_candies_with_price_mock.aggregate.assert_called_once_with(total=sum_patch())
        total_price_mock.__getitem__.assert_called_once_with('total')
        self.assertEqual(result, total_price_mock['total'])
        f_patch.assert_called_once_with('price')

    @patch('candy.services.candy_services.F')
    @patch('candy.services.candy_services.OrderServices.get_order')
    def test_get_candies_with_price(self, order_services_get_order_patch, f_patch):

        order_id_mock = MagicMock()
        order_mock = MagicMock()
        candies_price_mock = MagicMock()
        order_services_get_order_patch.return_value = order_mock
        order_mock.candy_amounts.all().annotate.return_value = candies_price_mock

        result = CandyServices.get_candies_with_price(order_id_mock)

        self.assertEqual(result, candies_price_mock)
        order_services_get_order_patch.assert_called_once_with(order_id_mock)
        f_patch.assert_has_calls([call('quantity'), call('candy_id__cost')])
        order_mock.candy_amounts.all().annotate.assert_called_once_with(price=f_patch('quantity') * f_patch('candy_id__cost'))

    @patch('candy.services.candy_services.OrderServices.get_order')
    def test_get_candy_amount_all(self, get_order_patch):

        order_id_mock = MagicMock()
        order_mock = MagicMock()
        candy_amounts_all_mock = MagicMock()
        get_order_patch.return_value = order_mock
        order_mock.candy_amounts.all.return_value = candy_amounts_all_mock

        result = CandyServices.get_candy_amount_all(order_id_mock)

        self.assertEqual(result, candy_amounts_all_mock)
        get_order_patch.assert_called_once_with(order_id_mock)
        order_mock.candy_amounts.all.assert_called_once_with()

    @patch('candy.services.candy_services.CandyServices.get_candy_amount')
    def test_update_candy_amount(self, get_candy_amount_patch):
        candy_amount_id_mock = MagicMock()
        quantity_mock = MagicMock()
        candy_amount_mock = MagicMock(quantity=1)
        get_candy_amount_patch.return_value = candy_amount_mock
        candy_amount_mock.quantity = quantity_mock

        CandyServices.update_candy_amount(candy_amount_id_mock, quantity_mock)

        get_candy_amount_patch.assert_called_once_with(candy_amount_id_mock)
        self.assertEqual(candy_amount_mock.quantity, quantity_mock)
        candy_amount_mock.save.assert_called_once_with()
