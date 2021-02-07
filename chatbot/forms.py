from django.forms import ModelForm
from django import forms
from.models import *


class CreateUserForm(ModelForm):
    class Meta:
        model=UserData
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput() ,
            'password2': forms.PasswordInput() 

        }
