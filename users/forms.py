from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms

class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')

class UserCreationChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email',)
