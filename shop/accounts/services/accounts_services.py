from candy.models import UserProfile
from django.contrib.auth.models import User
from django.template import loader
from django.core.mail import send_mail


class AccountsServices:

    @staticmethod
    def create_use_profile(user, phone):
        return UserProfile.objects.create(phone=phone, user=user)

    @staticmethod
    def get_admin_emails():
        email_list = []
        admins = User.objects.filter(is_superuser=1)
        for admin in admins:
            email_list.append(admin.email)
        return email_list

    @staticmethod
    def email_send(email, total_price, order_candies_with_price):
        html_message = loader.render_to_string(
            'email.html', {'total_price': total_price, 'order_candies_with_price': order_candies_with_price})
        recipient_list = [email]
        admin_emails = AccountsServices.get_admin_emails()
        recipient_list += admin_emails
        send_mail(
            subject='Your order',
            message='',
            html_message=html_message,
            from_email='my@gmail.com',
            recipient_list=recipient_list,
            fail_silently=False,
        )
