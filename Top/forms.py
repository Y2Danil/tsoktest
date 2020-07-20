from django import forms
from django.forms import TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('username', 'password1', 'password2')
    widgets = {
      'username': TextInput(attrs={
        'placeholder': 'Ник',
        'class': 'username'
      }),
      'password1': TextInput(attrs={
        'placeholder': 'Пароль',
        'class': 'password1'
      })
    }