from candy.services import OrderServices
from unittest.mock import MagicMock, patch
from django.test import SimpleTestCase


class CandyServicesTestCase(SimpleTestCase):

    @patch('candy.services.order_services.Order')
    def test_get_order(self, order_model_patch):
        order_id_mock = MagicMock()
        order_mock = MagicMock()
        order_model_patch.objects.get.return_value = order_mock

        result = OrderServices.get_order(order_id_mock)

        self.assertEqual(result, order_mock)
        order_model_patch.objects.get.assert_called_once_with(pk=order_id_mock)

    @patch('candy.services.order_services.Order')
    def test_get_in_progress_order_for_user(self, order_model_patch):
        user_mock = MagicMock()
        order_mock = MagicMock()
        order_model_patch.objects.filter().first.return_value = order_mock
        order_model_patch.objects.filter.reset_mock()

        result = OrderServices.get_in_progress_order_for_user(user_mock)

        self.assertEqual(result, order_mock)
        order_model_patch.objects.filter.assert_called_once_with(user=user_mock, status=order_model_patch.IN_PROGRESS)
        order_model_patch.objects.filter().first.assert_called_once_with()

    @patch('candy.services.order_services.Order')
    def test_create_order_row_auth(self, order_model_patch):
        user_mock = MagicMock(first_name='first_name', last_name='last_name', email='email')
        order_mock = MagicMock()
        firstname = user_mock.first_name
        lastname = user_mock.last_name
        email = user_mock.email
        order_model_patch.objects.create.return_value = order_mock

        result = OrderServices.create_order_row_auth(user_mock)

        self.assertEqual(result, order_mock)
        order_model_patch.objects.create.assert_called_once_with(firstname=firstname, lastname=lastname, email=email,
                                    status=order_model_patch.IN_PROGRESS, user=user_mock)

    @patch('candy.services.order_services.Order')
    def test_create_order_row_not_auth(self, order_model_patch):
        order_mock = MagicMock()
        order_model_patch.objects.create.return_value = order_mock

        result = OrderServices.create_order_row_not_auth()

        self.assertEqual(result, order_mock)
        order_model_patch.objects.create.assert_called_once_with(status=order_model_patch.IN_PROGRESS)

    @patch('candy.services.order_services.OrderServices.create_order_row_not_auth')
    @patch('candy.services.order_services.OrderServices.get_order')
    @patch('candy.services.order_services.OrderServices.create_order_row_auth')
    @patch('candy.services.order_services.OrderServices.get_in_progress_order_for_user')
    def test_get_or_create_order_auth_order(self, get_in_progress_order_for_user_patch, create_order_row_auth_patch,
                                            get_order_patch, create_order_row_not_auth_patch):
        user_mock = MagicMock(is_authenticated=True)
        order_mock = MagicMock()
        order_id_mock = MagicMock()
        get_in_progress_order_for_user_patch.return_value = order_mock

        result = OrderServices.get_or_create_order(user_mock, order_id_mock)

        self.assertEqual(result, order_mock)
        get_in_progress_order_for_user_patch.assert_called_once_with(user_mock)
        create_order_row_auth_patch.assert_not_called()
        get_order_patch.assert_not_called()
        create_order_row_not_auth_patch.assert_not_called()

    @patch('candy.services.order_services.OrderServices.create_order_row_not_auth')
    @patch('candy.services.order_services.OrderServices.get_order')
    @patch('candy.services.order_services.OrderServices.create_order_row_auth')
    @patch('candy.services.order_services.OrderServices.get_in_progress_order_for_user')
    def test_get_or_create_order_auth(self, get_in_progress_order_for_user_patch, create_order_row_auth_patch,
                                      get_order_patch, create_order_row_not_auth_patch):
        user_mock = MagicMock(is_authenticated=True)
        order_mock = MagicMock()
        order_id_mock = MagicMock()
        get_in_progress_order_for_user_patch.return_value = False
        create_order_row_auth_patch.return_value = order_mock

        result = OrderServices.get_or_create_order(user_mock, order_id_mock)

        self.assertEqual(result, order_mock)
        get_in_progress_order_for_user_patch.assert_called_once_with(user_mock)
        create_order_row_auth_patch.assert_called_once_with(user_mock)
        get_order_patch.assert_not_called()
        create_order_row_not_auth_patch.assert_not_called()

    @patch('candy.services.order_services.OrderServices.create_order_row_not_auth')
    @patch('candy.services.order_services.OrderServices.get_order')
    @patch('candy.services.order_services.OrderServices.create_order_row_auth')
    @patch('candy.services.order_services.OrderServices.get_in_progress_order_for_user')
    def test_get_or_create_order_not_auth(self, get_in_progress_order_for_user_patch, create_order_row_auth_patch,
                                          get_order_patch, create_order_row_not_auth_patch):
        user_mock = MagicMock(is_authenticated=False)
        order_mock = MagicMock()
        order_id_mock = MagicMock()
        get_order_patch.return_value = order_mock

        result = OrderServices.get_or_create_order(user_mock, order_id_mock)

        self.assertEqual(result, order_mock)
        get_in_progress_order_for_user_patch.assert_not_called()
        create_order_row_auth_patch.assert_not_called()
        get_order_patch.assert_called_once_with(order_id_mock)
        create_order_row_not_auth_patch.assert_not_called()

    @patch('candy.services.order_services.OrderServices.create_order_row_not_auth')
    @patch('candy.services.order_services.OrderServices.get_order')
    @patch('candy.services.order_services.OrderServices.create_order_row_auth')
    @patch('candy.services.order_services.OrderServices.get_in_progress_order_for_user')
    def test_get_or_create_order_not_auth_order(self, get_in_progress_order_for_user_patch,
                                                create_order_row_auth_patch,
                                                get_order_patch, create_order_row_not_auth_patch):
        user_mock = MagicMock(is_authenticated=False)
        order_mock = MagicMock()
        order_id_mock = None
        create_order_row_not_auth_patch.return_value = order_mock

        result = OrderServices.get_or_create_order(user_mock, order_id_mock)

        self.assertEqual(result, order_mock)
        get_in_progress_order_for_user_patch.assert_not_called()
        create_order_row_auth_patch.assert_not_called()
        get_order_patch.assert_not_called()
        create_order_row_not_auth_patch.assert_called_once_with()

    @patch('candy.services.order_services.Order')
    @patch('candy.services.order_services.OrderServices.get_order')
    def test_update_order(self, get_order_patch, order_model_patch):

        order_id_mock = MagicMock()
        order_model_patch_mock = MagicMock(DELIVERY='in_progress')
        order_model_patch.return_value = order_model_patch_mock
        order_mock = MagicMock()
        data = {'firstname': 'firstname', 'lastname': 'lastname', 'email': 'email', 'delivery_time': 'delivery_time',
                'address': 'address', 'phone': 'phone', 'comment': 'comment'}
        get_order_patch.return_value = order_mock

        result = OrderServices.update_order(order_id_mock, data)

        self.assertEqual(result, order_mock)
        self.assertEqual(data['firstname'], order_mock.firstname)
        self.assertEqual(data['lastname'], order_mock.lastname)
        self.assertEqual(data['email'], order_mock.email)
        self.assertEqual(data['delivery_time'], order_mock.delivery_time)
        self.assertEqual(data['address'], order_mock.address)
        self.assertEqual(data['phone'], order_mock.phone)
        self.assertEqual(order_model_patch.DELIVERY, order_mock.status)
        self.assertEqual(data['comment'], order_mock.comment)
        get_order_patch.assert_called_once_with(order_id_mock)
        order_mock.save.assert_called_once_with()
