#   User class imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

#   UserManager imports
from django.contrib.auth.base_user import BaseUserManager

#   Common Imports
from django.utils.translation import gettext_lazy as _ 

class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name,password=None):
        if not email:
            raise ValueError('Must have Email')
        if not username:
            raise ValueError('Must have username')
        if not first_name:
            raise ValueError('Must have first_name')
        if not last_name:
            raise ValueError('Must have last name')
        
        user    = self.model(
            email       = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):

        user =  self.create_user(
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password, 
        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user    

class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255,unique=True)
    username    = models.CharField(unique=True,  max_length=255,  null=True, blank=False)
    first_name  = models.CharField(unique=False, max_length=255,  null=True, blank=False, verbose_name='First Name')
    last_name   = models.CharField(unique=False, max_length=255,  null=True, blank=False, verbose_name='Last Name')
    date_joined = models.DateTimeField(default=timezone.now)

    is_staff    = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)

    USERNAME_FIELD  =   'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    def __str__(self):
        return f'{self. username} | {self.email}'

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return self.is_admin
