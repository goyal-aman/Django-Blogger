#   User class imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

#   UserManager imports
from django.contrib.auth.base_user import BaseUserManager

#   Common Imports
from django.utils.translation import gettext_lazy as _ 


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password, **extra_fields):
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
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password, 
            **extra_fields
        )
    

class User(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(max_length=255,unique=True)
    username    = models.CharField(unique=True,  max_length=255,  null=True, blank=False)
    first_name  = models.CharField(unique=False, max_length=255,  null=True, blank=False, verbose_name='First Name')
    last_name   = models.CharField(unique=False, max_length=255,  null=True, blank=False, verbose_name='Last Name')

    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD  =   'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    def __str__(self):
        return self.email