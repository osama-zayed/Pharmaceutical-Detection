from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="البريد الإلكتروني",error_messages={'required': 'البريد الإلكتروني مطلوب'}) 
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2','email')