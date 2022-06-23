from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.
class User(AbstractUser):
    is_customer=models.BooleanField(default=False)
    is_gate=models.BooleanField(default=False)
    is_cctv=models.BooleanField(default=False)
    is_restaurant=models.BooleanField(default=False)
    class Meta:        
        verbose_name="All User"
    

class gatekeepers(User):
    class Meta:
        proxy = True
        verbose_name="GATEkeeper"

# class store(models.Model):
#     Name=models.CharField(null=False,default='store-x')
#     Floor=models.IntegerField(null=False, default=0)
#     open_time=models.TimeField(null=False,default=datetime.time(9, 00))
#     close_time=models.TimeField(null=False,default=datetime.time(19, 00))