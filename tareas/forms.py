from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tarea


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['title', 'description']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

