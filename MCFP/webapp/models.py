from email.policy import default
from numbers import Rational
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from start.models import User

# class User(AbstractUser):
# 	is_customer   = models.BooleanField(default=False)
# 	is_restaurant = models.BooleanField(default=False)


class Customer(models.Model):
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	f_name   	= models.CharField(max_length=20,blank=False,verbose_name='First Name')
	l_name		= models.CharField(max_length=20,blank=False,verbose_name='Last Name')
	# city  		= models.CharField(max_length=40,blank=False)
	phone 		= models.IntegerField(blank=False,unique=True,verbose_name='Mobile')
	
	def __str__(self):
		return self.user.username
	
class Restaurant(models.Model):
	user        = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	rname 		= models.CharField(max_length=20,blank=False,verbose_name='Restaurant')
	info	 	= models.CharField(max_length=40,blank=False,verbose_name='Restaurant Info')
	# min_ord		= models.CharField(max_length=5,blank=False)
	location    = models.CharField(max_length=10,blank=False,unique=True)
	r_logo      = models.FileField(blank=False)

	REST_STATE_OPEN    = "Open"
	REST_STATE_CLOSE   = "Closed"
	REST_STATE_CHOICES =(
			(REST_STATE_OPEN,REST_STATE_OPEN),
			(REST_STATE_CLOSE,REST_STATE_CLOSE)
		)
	status 	= models.CharField(max_length=50,choices=REST_STATE_CHOICES,default=REST_STATE_OPEN,blank=False)
	# approved = models.BooleanField(blank=False,default=True)

	def __str__(self):
		return self.rname
		
class Item(models.Model):
	id 			= models.AutoField(primary_key=True)
	fname 		= models.CharField(max_length=30,blank=False,unique=True,verbose_name='Item')
	category 	= models.CharField(max_length=50,blank=False)
	rid			= models.IntegerField(null=False,default=-1,verbose_name='Restaurant')
	img			=models.ImageField(blank=False)


	def __str__(self):
		return self.fname

class Menu(models.Model):
	id 		 = models.AutoField(primary_key=True)
	item_id  = models.ForeignKey(Item,on_delete=models.CASCADE,verbose_name='Item Name')
	r_id     = models.ForeignKey(Restaurant,on_delete=models.CASCADE,verbose_name='Restaurant')
	price    = models.IntegerField(blank=False)
	quantity = models.IntegerField(blank=False,default=0)

	def __str__(self):
		return self.item_id.fname+'   - '+str(self.price)+'\t \ Piece'
	

class Order(models.Model):
	id 				= models.AutoField(primary_key=True)
	total_amount    = models.IntegerField(default=0,verbose_name='Total Amount')
	timestamp       = models.DateTimeField(auto_now_add=True,verbose_name='Time')
	delivery_addr   = models.IntegerField(null=False,blank=True,default=-1,verbose_name='Table Number')
	orderedBy       = models.ForeignKey(User ,on_delete=models.CASCADE)
	r_id			= models.ForeignKey(Restaurant ,on_delete=models.CASCADE,verbose_name='Restaurant')
	# pay_status		=models.BooleanField(null=False,default=False)
	
	
	ORDER_STATE_WAITING 	 = "Waiting"
	ORDER_STATE_PLACED 		 = "Placed"
	ORDER_STATE_ACKNOWLEDGED = "Acknowledged"
	ORDER_STATE_COMPLETED    = "Completed"
	ORDER_STATE_CANCELLED    = "Cancelled"
	ORDER_STATE_DISPATCHED   = "Dispatched"

	ORDER_STATE_CHOICES = (
		(ORDER_STATE_WAITING,ORDER_STATE_WAITING),
	    (ORDER_STATE_PLACED, ORDER_STATE_PLACED),
	    (ORDER_STATE_ACKNOWLEDGED, ORDER_STATE_ACKNOWLEDGED),
	    (ORDER_STATE_COMPLETED, ORDER_STATE_COMPLETED),
	    (ORDER_STATE_CANCELLED, ORDER_STATE_CANCELLED),
	    (ORDER_STATE_DISPATCHED, ORDER_STATE_DISPATCHED)
	)
	status = models.CharField(max_length=50,choices=ORDER_STATE_CHOICES,default=ORDER_STATE_WAITING)
	
	def __str__(self):
		return str(self.id) +' '+self.status


class orderItem(models.Model):
	id 			= models.AutoField(primary_key=True)
	item_id 	= models.ForeignKey(Menu ,on_delete=models.CASCADE)
	ord_id  	= models.ForeignKey(Order,on_delete=models.CASCADE)
	quantity 	= models.IntegerField(default=0)
	
	def __str__(self):
		return str(self.id) 


class Feedback(models.Model):
	customer=models.ForeignKey(User,on_delete=models.CASCADE)
	remarks=models.TextField(max_length=200)
	rating=models.IntegerField(default=0)
	orderid=models.ForeignKey(Order,on_delete=models.DO_NOTHING,default=1)








		
		



		

