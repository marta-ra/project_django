from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .services import AccountsServices


class SignUpForm(UserCreationForm):
    phone = forms.CharField(
        max_length=255,
        required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        phone = self.cleaned_data['phone']
        AccountsServices.create_use_profile(user, phone)
        return user

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
