from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,AbstractUser
from django import forms
from .models import CustomUser

class SignUp(UserCreationForm):
    first_name=forms.CharField(max_length=20)
    last_name=forms.CharField(max_length=30)
    email=forms.EmailField()

    class Meta:
        model=CustomUser
        fields=['first_name','last_name','username','email','password1','password2']

class ProfileForm(forms.ModelForm):
    first_name=forms.CharField(max_length=20)
    last_name=forms.CharField(max_length=30)
    class Meta:
         model=CustomUser
         fields=['first_name','last_name','age','daily_goals']