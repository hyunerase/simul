from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserPro(AbstractUser):
    access_token = models.CharField(max_length=225, blank=True, null=True)
    nickname = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/', null=True, blank=True)