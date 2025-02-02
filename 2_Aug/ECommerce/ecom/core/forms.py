from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms 

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    username = forms.CharField(widget=forms.TextInput(attrs={
            'class':'form-control'
        }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
            'class':'form-control'
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class':'form-control'
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class':'form-control'
        }))
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
            'class':'form-control'
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class':'form-control'
        }))
   