from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False, label="Номер телефона")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Адрес доставки")
    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model = User
        fields = ['username', 'address', 'phone', 'email', 'password1', 'password2']
