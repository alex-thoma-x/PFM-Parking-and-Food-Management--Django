from wsgiref.validate import validator
from django.contrib.auth.forms import UserCreationForm
from django import forms
from js2py import require
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re
from .models import *

def usr_name(value):
	pattern = re.compile("^[a-zA-Z]{3,}$")
	#"^[A-Za-z]\\w{5, 29}$"
	if  len(value)>30 or len(value)<3:
		raise ValidationError("Min 4 and Max 12 Characters")
	if not pattern.match(value):
		raise ValidationError("Only Alphabets")
		
def rest_name(value):
	pattern = re.compile("^[a-zA-Z]{3,}$")
	#"^[A-Za-z]\\w{5, 29}$"
	if  len(value)>30 or len(value)<=2:
		raise ValidationError("Min 2 and Max 12 Characters")
	if not pattern.match(value):
		raise ValidationError("Only Alphabets and min 6 and max 30 Charcters")


def passw(value):
	if validate_password(value):
		raise ValidationError("Min 8 Charracters")

def mobile(value):
  if len(value) < 10 or not value.isdigit() or len(value)>12:
    raise ValidationError("Invalid Mobile")

def feedback(value):
	pattern = re.compile("^[a-zA-Z]{3,}$")
	#"^[A-Za-z]\\w{5, 29}$"
	if  len(value)>199 or len(value)<4:
		raise ValidationError("Min 4 and Max 200 Characters")
	if not pattern.match(value):
		raise ValidationError("Only Alphabets")


# def store_loc(value):
# 	s=set()
# 	r=Restaurant.objects.location()
# 	for i in r:
# 		s.add(i)
# 	if value in s:
# 		raise ValidationError("Location Already Exist")




class CustomerSignUpForm(forms.ModelForm):
	username = forms.CharField(initial = "username",max_length = 12,validators=[usr_name])
	password = forms.CharField(widget=forms.PasswordInput,validators=[passw])
	email	 = forms.CharField(required=True)
	
	class Meta:
		model = User
		fields=['username','email','password']
													
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
	rname = forms.CharField(initial = "Restaurant Name",max_length = 14,required = True,validators=[rest_name])
	# location=forms.CharField(validators=['store_loc'])
	class Meta:
		model = Restaurant
		fields =['rname','info','location','r_logo']

cat_choices =(
("Arabian", "Arabian"),
("Indian", "Indian"),
("Biriyani","Biriyani"),
("Pizza",'Pizza'),
("Italian","Italian"),
('Snacks','Snacks')
)

class itemadd(forms.ModelForm):
	fname = forms.CharField(initial = "Item",max_length = 12,required = True,validators=[usr_name])
	category=forms.ChoiceField(choices=cat_choices,required=True)
	class Meta:
		model = Item
		fields =['fname','category','img']







		
		

			




		
		


