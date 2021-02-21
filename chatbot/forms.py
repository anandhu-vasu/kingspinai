from django.forms import ModelForm
from django import forms
from.models import *


class CreateUserForm(ModelForm):
    
    class Meta:
        model=UserData
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
             'name'   :forms.TextInput(attrs={'class':'form-control'}) ,
             'lastname'   :forms.TextInput(attrs={'class':'form-control'}),
             'email'   :forms.TextInput(attrs={'class':'form-control'}),
             'city'   :forms.TextInput(attrs={'class':'form-control'}),
             'postalcode'   :forms.TextInput(attrs={'class':'form-control '}),
             'country'   :forms.Select(attrs={'class':'form-control selectric'}),
             'company'   :forms.TextInput(attrs={'class':'form-control'}),

        }
