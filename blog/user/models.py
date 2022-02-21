from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    web_personal= models.CharField(max_length=30, blank=True, null=True)