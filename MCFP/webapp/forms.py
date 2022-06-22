from wsgiref.validate import validator
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User,Customer,Restaurant,Item,Menu
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re

def usr_name(value):
	pattern = re.compile("/^[A-Za-z]+$/")
	#"^[A-Za-z]\\w{5, 29}$"
	if not pattern.match(value) or len(value)>30 or len(value)<6:
		raise ValidationError("Only Alphabets and min 6 and max 30 Charcters")
		

def passw(value):
	if validate_password(value):
		raise ValidationError("Min 8 Charracters")

def mobile(value):
  if len(value) < 10 or not value.isdigit() or len(value)>12:
    raise ValidationError("Invalid Mobile")


class CustomerSignUpForm(forms.ModelForm):
	username = forms.CharField(initial = "username",max_length = 12,validators=[usr_name])
	password = forms.CharField(widget=forms.PasswordInput,validators=[passw])
	email	 = forms.CharField(required=True)
	
	class Meta:
		model = User
		fields=['username','email','password']
		
		help_texts = {
            'password': _('Min 8 characters'),
        }
		
							
							
	


		def save(self, commit=True):
			user = super().save(commit=False)
			user.is_customer=True
			if commit:
				user.save()
			return user
		

class RestuarantSignUpForm(forms.ModelForm):
	username = forms.CharField(initial = "username",max_length = 12,required = True,validators=[usr_name])
	password = forms.CharField(widget=forms.PasswordInput,validators=[passw])
	email	 = forms.CharField(required=True)
	class Meta:
		model =User
		fields=['username','email','password']
		
		def save(self,commit=True):
			user=super().save(commit=False)
			user.is_restaurant=True
			if commit:
				user.save()
			return user


class CustomerForm(forms.ModelForm):
	f_name = forms.CharField(initial = "FirsName",max_length = 12,required = True,validators=[usr_name])
	l_name = forms.CharField(initial = "LastName",max_length = 12,required = True,validators=[usr_name])
	phone	 = forms.CharField(initial = "Mobile",required = True,validators=[mobile])
	class Meta:
		model = Customer
		fields =['f_name','l_name','phone']
		labels = {'f_name': _('First Name'),'l_name':_('Last Name'),'phone':_('phone') }
		
		
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }
		


class RestuarantForm(forms.ModelForm):
	rname = forms.CharField(initial = "Restaurant Name",max_length = 14,required = True,validators=[usr_name])
	class Meta:
		model = Restaurant
		fields =['rname','info','location','r_logo','min_ord']


class itemadd(forms.ModelForm):
	class Meta:
		model = Item
		fields =['fname','category','img']






		
		

			




		
		


