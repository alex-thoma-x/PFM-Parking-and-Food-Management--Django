from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_customer=models.BooleanField(default=False)
    is_gate=models.BooleanField(default=False)
    is_cctv=models.BooleanField(default=False)
    is_restaurant=models.BooleanField(default=False)