
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import User
  
class UserRegistrationForm(UserCreationForm): 
    name =  forms.CharField(label = "Full name")
    class Meta: 
        model = User 
        fields = ('email','name','company_name','phone','password1','password2')
        
class UserLoginForm(forms.ModelForm):
    password=forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=('email','password')


    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password=self.cleaned_data['password']
            
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid Credential")

        
