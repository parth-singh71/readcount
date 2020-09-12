from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        # fields = ['username', 'password1', 'password2']
        fields = ['username', 'password']


# class UserUpdateForm(form.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username']
