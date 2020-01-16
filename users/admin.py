from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Profile, Follow
# Register your models here.
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form    = UserChangeForm
    model   = User

    list_display = ('email','username','first_name','last_name', 'is_active','is_admin','is_staff')
    list_filter = ('email', 'username','is_active','is_staff', 'is_admin',)
    fieldsets = (
        (None, {'fields': ('email','username','first_name','last_name','password',)}),
        ('Permissions', {'fields': ('is_active','is_staff', 'is_admin',)})
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email','username','first_name','last_name','password1','password2','is_active','is_staff', 'is_admin')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Follow)