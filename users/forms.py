from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name','username',)

class UserCreationChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name','username',)
