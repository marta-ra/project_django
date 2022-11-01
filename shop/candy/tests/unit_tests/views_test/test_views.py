from candy.views import *
from unittest.mock import MagicMock, patch
from django.test import SimpleTestCase


class CandyTestCase(SimpleTestCase):

    @patch('candy.views.render')
    @patch('candy.views.CategoryServices.get_categories')
    def test_main(self, get_categories_patch, render_patch):
        categories_mock = MagicMock()
        request_mock = MagicMock(method='GET')
        get_categories_patch.return_value = categories_mock
        render_mock = MagicMock()
        render_patch.return_value = render_mock
        context = {'categories': categories_mock}

        result = main(request_mock)

        self.assertEqual(result, render_mock)
        get_categories_patch.assert_called_once_with()
        render_patch.assert_called_once_with(request_mock, 'main.html', context)

    @patch('candy.views.render')
    @patch('candy.views.CandyServices.get_candies_by_category')
    @patch('candy.views.CategoryServices.get_category')
    @patch('candy.views.AddCandyAmount')
    def test_candy_show(self, add_candy_amount_form_path, get_category_patch, get_candies_by_category_patch, render_patch):
        category_mock = MagicMock()
        category_id_mock = MagicMock()
        candies_mock = MagicMock()
        request_mock = MagicMock(method='GET')
        render_mock = MagicMock()
        add_candy_amount_form_path_mock = MagicMock()
        add_candy_amount_form_path.return_value = add_candy_amount_form_path_mock
        get_category_patch.return_value = category_mock
        get_candies_by_category_patch.return_value = candies_mock
        render_patch.return_value = render_mock
        context = {'candies': candies_mock, 'form': add_candy_amount_form_path_mock, 'category': category_mock}

        result = candy_show(request_mock, category_id_mock)

        self.assertEqual(result, render_mock)
        add_candy_amount_form_path.assert_called_once_with()
        get_category_patch.assert_called_once_with(category_id_mock)
        get_candies_by_category_patch.assert_called_once_with(category_mock)

        render_patch.assert_called_once_with(request_mock, 'candies.html', context)

    @patch('candy.views.Utils.check_time')
    @patch('candy.views.render')
    @patch('candy.views.Order')
    @patch('candy.views.CandyServices.get_sum_order')
    @patch('candy.views.CandyServices.get_candies_with_price')
    @patch('candy.views.OrderServices.get_or_create_order')
    def test_order_show_auth(self, get_or_create_order_patch, get_candies_with_price_patch, get_sum_order_patch,
                             order_form_patch, render_patch, check_time_patch):

        order_mock = MagicMock()
        order_candies_with_price_mock = MagicMock()
        total_price_mock = MagicMock()
        render_mock = MagicMock()
        order_form_patch_mock = MagicMock()
        check_time_mock = MagicMock()
        check_time_patch.return_value = check_time_mock
        user_mock = MagicMock(is_authenticated=True, total_price=total_price_mock,
                              order_candies_with_price=order_candies_with_price_mock)

        request_mock = MagicMock(method='GET', user=user_mock, session={'order_id': 'order_id'})
        default_values = {'firstname': request_mock.user.first_name, 'email': request_mock.user.email,
                          'lastname': request_mock.user.last_name, 'phone': request_mock.user.users_profile.phone,
                          'total_price': total_price_mock, 'order_candies_with_price': order_candies_with_price_mock}
        order_form_patch.return_value = order_form_patch_mock
        get_or_create_order_patch.return_value = order_mock
        get_candies_with_price_patch.return_value = order_candies_with_price_mock
        get_sum_order_patch.return_value = total_price_mock

        render_patch.return_value = render_mock
        context = {'form': order_form_patch_mock, 'total_price': total_price_mock,
                   'order_candies_with_price': order_candies_with_price_mock,
                   'time_allow': check_time_mock}

        result = order_show(request_mock)

        self.assertEqual(result, render_mock)
        get_or_create_order_patch.assert_called_once_with(request_mock.user, request_mock.session.get('order_id'))
        order_form_patch.assert_called_once_with(default_values)
        get_candies_with_price_patch.assert_called_once_with(order_mock.id)
        get_sum_order_patch.assert_called_once_with(order_candies_with_price_mock)
        render_patch.assert_called_once_with(request_mock,  'order.html', context)

    @patch('candy.views.Utils.check_time')
    @patch('candy.views.render')
    @patch('candy.views.Order')
    @patch('candy.views.CandyServices.get_sum_order')
    @patch('candy.views.CandyServices.get_candies_with_price')
    @patch('candy.views.OrderServices.get_or_create_order')
    def test_order_show_not_auth(self, get_or_create_order_patch, get_candies_with_price_patch, get_sum_order_patch,
                                 order_form_patch, render_patch, check_time_patch):
        order_mock = MagicMock()
        order_candies_with_price_mock = MagicMock()
        total_price_mock = MagicMock()
        render_mock = MagicMock()
        order_form_patch_mock = MagicMock()
        check_time_mock = MagicMock()
        check_time_patch.return_value = check_time_mock
        user_mock = MagicMock(is_authenticated=False, total_price=total_price_mock,
                              order_candies_with_price=order_candies_with_price_mock)

        request_mock = MagicMock(method='GET', user=user_mock, session={'order_id': 'order_id'})
        order_form_patch.return_value = order_form_patch_mock
        get_or_create_order_patch.return_value = order_mock
        get_candies_with_price_patch.return_value = order_candies_with_price_mock
        get_sum_order_patch.return_value = total_price_mock

        render_patch.return_value = render_mock
        context = {'form': order_form_patch_mock, 'total_price': total_price_mock,
                   'order_candies_with_price': order_candies_with_price_mock,
                   'time_allow': check_time_mock}

        result = order_show(request_mock)

        self.assertEqual(result, render_mock)
        get_or_create_order_patch.assert_called_once_with(request_mock.user, request_mock.session.get('order_id'))
        order_form_patch.assert_called_once_with()
        get_candies_with_price_patch.assert_called_once_with(order_mock.id)
        get_sum_order_patch.assert_called_once_with(order_candies_with_price_mock)
        render_patch.assert_called_once_with(request_mock, 'order.html', context)

    @patch('candy.views.AccountsServices.email_send')
    @patch('candy.views.render')
    @patch('candy.views.Order')
    @patch('candy.views.CandyServices.get_sum_order')
    @patch('candy.views.CandyServices.get_candies_with_price')
    @patch('candy.views.OrderServices.update_order')
    @patch('candy.views.OrderServices.get_or_create_order')
    def test_order_confirm(self, get_or_create_order_patch, update_order_patch, get_candies_with_price_patch,
                           get_sum_order_patch, order_form_patch, render_patch, email_send_patch):
        order_id_mock = MagicMock()
        order_mock = MagicMock()
        order_candies_with_price_mock = MagicMock()
        total_price_mock = MagicMock()
        render_mock = MagicMock()
        order_form_patch_mock = MagicMock(cleaned_data={'email': ''})
        data = order_form_patch_mock.cleaned_data
        user_mock = MagicMock()
        request_mock = MagicMock(method='POST', user=user_mock)
        order_form_patch.return_value = order_form_patch_mock
        get_or_create_order_patch.return_value = order_id_mock
        update_order_patch.return_value = order_mock
        get_candies_with_price_patch.return_value = order_candies_with_price_mock
        get_sum_order_patch.return_value = total_price_mock

        render_patch.return_value = render_mock
        context = {'order': order_mock, 'total_price': total_price_mock,
                   'order_candies_with_price': order_candies_with_price_mock}

        result = order_confirm(request_mock)

        self.assertEqual(result, render_mock)
        order_form_patch.assert_called_once_with(request_mock.POST)
        order_form_patch_mock.is_valid.assert_called_once_with()
        get_or_create_order_patch.assert_called_once_with(request_mock.user, request_mock.session.get('order_id'))
        update_order_patch.assert_called_once_with(order_id_mock.id, data)
        get_candies_with_price_patch.assert_called_once_with(order_id_mock.id)
        get_sum_order_patch.assert_called_once_with(order_candies_with_price_mock)
        email_send_patch.assert_called_once_with(data['email'], total_price_mock, order_candies_with_price_mock)
        render_patch.assert_called_once_with(request_mock, 'order_confirmed.html', context)

    @patch('candy.views.redirect')
    @patch('candy.views.CandyServices.create_candy_amount')
    @patch('candy.views.Utils.session_data')
    @patch('candy.views.OrderServices.get_or_create_order')
    @patch('candy.views.CandyServices.get_candy')
    @patch('candy.views.AddCandyAmount')
    def test_add_candy_not_auth(self, add_candy_amount_form_patch, get_candy_patсh, get_or_create_order_patch,
                                session_data_patch, create_candy_amount_patch, redirect_patch):
        candy_id_mock = MagicMock()
        category_id_mock = MagicMock()
        user_mock = MagicMock(is_authenticated=False)
        request_mock = MagicMock(method='POST', user=user_mock)
        add_candy_amount_form_patch_mock = MagicMock(cleaned_data={'amount': ''})
        add_candy_amount_form_patch.return_value = add_candy_amount_form_patch_mock
        data = add_candy_amount_form_patch_mock.cleaned_data
        amount = data['amount']
        candy_mock = MagicMock()
        order_mock = MagicMock()
        get_candy_patсh.return_value = candy_mock
        get_or_create_order_patch.return_value = order_mock
        candy_amount_mock = MagicMock()
        create_candy_amount_patch.return_value = candy_amount_mock
        redirect_mock = MagicMock()
        redirect_patch.return_value = redirect_mock

        result = add_candy(request_mock, candy_id_mock, category_id_mock)

        self.assertEqual(result, redirect_mock)
        add_candy_amount_form_patch.assert_called_once_with(request_mock.POST)
        add_candy_amount_form_patch_mock.is_valid.assert_called_once_with()
        get_candy_patсh.assert_called_once_with(candy_id_mock)
        get_or_create_order_patch.assert_called_once_with(request_mock.user, request_mock.session.get('order_id'))
        session_data_patch.assert_called_once_with(request_mock, order_mock.id)
        create_candy_amount_patch.assert_called_once_with(order_mock, candy_mock, amount)
        redirect_patch.assert_called_once_with(candy_show, category_id=category_id_mock)

    @patch('candy.views.redirect')
    @patch('candy.views.CandyServices.update_candy_amount')
    def test_update_candy_amount(self, update_candy_amount_patch, redirect_patch):
        candy_amount_id_mock = MagicMock()
        request_mock = MagicMock(method='POST', POST={'quantity': ''})
        quantity = request_mock.POST['quantity']
        redirect_mock = MagicMock()
        redirect_patch.return_value = redirect_mock

        result = update_candy_amount(request_mock, candy_amount_id_mock)

        self.assertEqual(result, redirect_mock)
        update_candy_amount_patch.assert_called_once_with(candy_amount_id_mock, quantity)
        redirect_patch.assert_called_once_with(order_show)
