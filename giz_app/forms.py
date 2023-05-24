from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none',
                                      'placeholder': 'First Name', 'rows': 5}), label='First Name')

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none',
                                      'placeholder': 'Last Name', 'rows': 5}), label='Last Name')

    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none',
                                      'placeholder': 'Email', 'rows': 5}), label='Email')

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none',
                                      'placeholder': 'Username', 'rows': 5}), label='Name')

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control shadow-none',
                                          'placeholder': 'Password', 'rows': 5}), label='Password')

    password2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none',
                                      'placeholder': 'Repeat Password', 'rows': 5}), label='Repeat Password')

    # levels = forms.SelectMultiple()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', ]
