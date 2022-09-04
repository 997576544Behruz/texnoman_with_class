from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
from texnoman.models import UserProfile


class SignUpForm(UserCreationForm):
    class Meta:
        model=UserProfile
        fields=('username','password1','password2','email','address','image')
class UserProfileForm(UserChangeForm):
    class Meta:
        model=UserProfile
        fields=['username', 'first_name', 'last_name', 'image', 'bio',
                'birthday', 'address', 'phone_number']