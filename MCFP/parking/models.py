from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class parking_slots(models.Model):
    user 		= models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Total_Slots = models.IntegerField(null=False,default=20)
    parked       =models.IntegerField(null=False,default=0)
	
   


class Category(models.Model):
    categoryname = models.CharField(max_length=50)
    def __str__(self):
        return self.categoryname



class Vehicle(models.Model):

    id=models.AutoField(primary_key=True)
    gate=models.CharField(null=False,max_length=8,default="main")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    regno = models.CharField(max_length=10)
    ownercontact = models.CharField(max_length=15)
    pdate = models.DateTimeField(null=False)
    intime = models.CharField(max_length=50)
    outtime = models.CharField(max_length=50)
    parkingcharge = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    def __int__(self):
        return self.id




