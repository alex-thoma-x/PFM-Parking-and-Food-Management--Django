from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User,Customer,Restaurant,Item,Menu
from django.utils.translation import gettext_lazy as _

class CustomerSignUpForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
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
	password = forms.CharField(widget=forms.PasswordInput)
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
	class Meta:
		model = Restaurant
		fields =['rname','info','location','r_logo','min_ord']


class itemadd(forms.ModelForm):
	class Meta:
		model = Item
		fields =['fname','category','img']






		
		

			




		
		


