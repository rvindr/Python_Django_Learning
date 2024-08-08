from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class CustomUser(AbstractUser):

    username = None
    phone_number = models.CharField(max_length=12, unique=True)
    profile_img = models.ImageField(blank=True, null=True, upload_to='profile')
    id_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS=[]

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()