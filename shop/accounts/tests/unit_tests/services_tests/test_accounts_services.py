from accounts.services import AccountsServices
from unittest.mock import MagicMock, patch
from django.test import SimpleTestCase


class AccountsServicesTestCase(SimpleTestCase):

    @patch('accounts.services.accounts_services.UserProfile')
    def test_create_use_profile(self, user_profile_model_patch):
        user_mock = MagicMock()
        phone_mock = MagicMock()
        user_profile_mock = MagicMock()
        user_profile_model_patch.objects.create.return_value = user_profile_mock

        result = AccountsServices.create_use_profile(user_mock, phone_mock)

        self.assertEqual(result, user_profile_mock)
        user_profile_model_patch.objects.create.assert_called_once_with(phone=phone_mock, user=user_mock)

    @patch('accounts.services.accounts_services.User')
    def test_get_admin_emails(self, user_model_patch):
        email_list = []
        admins_mock = [MagicMock(email='email')]
        user_model_patch.objects.filter.return_value = admins_mock
        for admin in admins_mock:
            email_list.append(admin.email)

        result = AccountsServices.get_admin_emails()

        self.assertEqual(result, email_list)
        user_model_patch.objects.filter.assert_called_once_with(is_superuser=1)

    @patch('accounts.services.accounts_services.send_mail')
    @patch('accounts.services.accounts_services.loader.render_to_string')
    @patch('accounts.services.accounts_services.AccountsServices.get_admin_emails')
    def test_get_admin_emails(self, get_admin_emails_patch, render_to_string_patch, send_mail_patch):
        html_message_mock = MagicMock()
        admin_emails_mock = [MagicMock()]
        email_mock = MagicMock()
        total_price_mock = MagicMock()
        order_candies_with_price_mock = MagicMock()
        render_to_string_patch.return_value = html_message_mock
        get_admin_emails_patch.return_value = admin_emails_mock
        recipient_list = [email_mock]

        AccountsServices.email_send(email_mock, total_price_mock, order_candies_with_price_mock)

        render_to_string_patch.assert_called_once_with('email.html', {'total_price': total_price_mock,
                                                       'order_candies_with_price': order_candies_with_price_mock})
        get_admin_emails_patch.assert_called_once_with()
        send_mail_patch.assert_called_once_with(
            subject='Your order',
            message='',
            html_message=html_message_mock,
            from_email='my@gmail.com',
            recipient_list=recipient_list + admin_emails_mock,
            fail_silently=False,)

