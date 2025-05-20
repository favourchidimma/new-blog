from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Create your models here


class User(AbstractBaseUser, PermissionsMixin):

    Role_Choices = (
        ('app_admin', 'App Admin'),
        ('root_admin', 'Root Admin'),
        ('super_admin', 'Super Admin'),
        ('user', 'User'),
    )

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=225, choices=Role_Choices)
    password = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    objects = UserManager()


class OTP(models.Model):
    otp = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()


    def is_otp_valid(self):
        return bool(self.expiry_date > timezone.now())
    

