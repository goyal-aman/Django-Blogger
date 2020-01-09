from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile
from django import forms

#for admin page
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')

#for admin page
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email',)

class UserUpdateForm(forms.ModelForm):
    '''
    model form are the form that work with specific user model
    '''
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email',)



class ProfileUpdateForm(forms.ModelForm):
    '''
    model form are the form that work with specific user model
    '''
    class Meta:
        model = Profile
        fields = ['image']

