from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Register

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Register
        fields = ['first_name','last_name',' username','email', 'password', 'password']
