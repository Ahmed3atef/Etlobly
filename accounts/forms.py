# forms.py
from django import forms
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ['email','name', 'DOB', 'phone_number','password1', 'password2']
        widgets = {
            'DOB': forms.DateInput(attrs={'type': 'date'}),
        }

    
        