from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class CustomUsers(AbstractUser):
    username = None

    phone_number = models.CharField(max_length=12, unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=4, default=0)
    USERNAME_FIELD = 'phone_number'

    objects = UserManager()