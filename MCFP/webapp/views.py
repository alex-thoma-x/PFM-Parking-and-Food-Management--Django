from itertools import count
from lib2to3.pgen2.tokenize import generate_tokens
from sqlite3 import Timestamp
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from .forms import CustomerSignUpForm,RestuarantSignUpForm,CustomerForm,RestuarantForm, feedback, itemadd
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.urls import reverse
from django.db.models import Q
from .models import  *
from start.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from parking.models import parking_slots
import json
import math, random
from django.http import JsonResponse
from parking.models import Vehicle
from parking.views import slotcheck



#### ---------- General Side -------------------#####

# Showing index page
def index(request):
	slots=parking_slots.objects.all()
	return render(request,'webapp/index.html',{'slots':slots})

#global variable for storing Orderid
order_id_for_otp=False

@login_required(login_url='food:index')
def orderplaced(request):
	if request.user.is_customer==False and request.user.is_superuser==False:
		return redirect('food:logout')
	if not order_id_for_otp:
		return redirect('food:restuarant')
	order=Order.objects.filter(id=int(order_id_for_otp))
	return render(request,'webapp/orderplaced.html',{'order':order[0].secret_code})


# Showing Restaurants list to Customer
def restuarent(request):
	# if request.user.is_customer==False and request.user.is_superuser==False:
	# 	return redirect('food:logout')
	r_object = Restaurant.objects.all()
	query 	= request.GET.get('q')
	if query:
		# r_object=Restaurant.objects.filter(Q(rname__icontains=query)).distinct()
		item=Item.objects.filter(fname__startswith=query).values_list('rid', flat=True)
		
		if item.count()!=0:
			r_object=Restaurant.objects.filter(id__in=item).distinct()
		else:
		# r_object=Restaurant.objects.filter(Q(rname__icontains=query)).distinct()
			r_object=Restaurant.objects.filter(rname__startswith=query).distinct()
		return render(request,'webapp/restaurents.html',{'r_object':r_object})
	return render(request,'webapp/restaurents.html',{'r_object':r_object})

#popmenu in restaurant list for customers
def popmenu(request):
	if request.method == 'POST':
		rid=json.loads(request.body).get('rid')
		menu = Menu.objects.filter(r_id=rid).values_list('item_id', flat=True)
		
		item = Item.objects.filter(id__in=menu)
		data=item.values()
			
		for y in list(data):
			m=Menu.objects.filter(item_id=y['id'])
			y['price']=m[0].price
			

				
		return JsonResponse(list(data), safe=False)

# logout
def Logout(request):
	if request.user.is_restaurant:
		logout(request)
		return redirect("food:rlogin")
	else:
		logout(request)
		return redirect("food:login")

		

#### -----------------Customer Side---------------------- ######

# Creating Customer Account
def customerRegister(request):
	form =CustomerSignUpForm(request.POST or None)
	if form.is_valid():
		user      = form.save(commit=False)
		username  =	form.cleaned_data['username']
		password  = form.cleaned_data['password']
		user.is_customer=True
		user.set_password(password)
		user.save()
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("food:ccreate")
	context ={
		'form':form
	}			
	return render(request,'webapp/signup.html',context)

# Customer Login
def customerLogin(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user     = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active and user.is_customer:
				login(request,user)
				return redirect('food:restuarant')
			else:
				return render(request,'webapp/login.html',{'error_message':'Your account disable or You are not permitted'})
		else:
			return render(request,'webapp/login.html',{'error_message': 'Invalid Login'})
	return render(request,'webapp/login.html')

# customer profile view
def customerProfile(request,pk=None):
	if request.user.is_customer==False:
		return redirect('food:logout')
	if pk:
		user = User.objects.get(pk=pk)
	else:
		user=request.user

	vehicle=Vehicle.objects.filter(ownercontact=user.customer.phone,status='In')	
	if vehicle.count()!=0:
		gate=vehicle[0].gate
		
	else:
		gate=False
	return render(request,'webapp/profile.html',{'user':user,'gate':gate})


#to find the parking slot of the registered user
@login_required(login_url='food:index')
def parkslot(request):
	user=request.user
	vehicle=Vehicle.objects.filter(ownercontact=user.customer.phone,status='In')	
	if vehicle.count()!=0:
		slots=vehicle[0].slot
		gate=vehicle[0].gate
		slot_for_user=slotcheck(gate)
		slot=[1]*20
		for i in range(20):
			if i+1 in slot_for_user:
				slot[i]=0
		slot[slots-1]=2
		print(slot)
		s1=slot[:10]
		s2=slot[10:]
		slot1 = dict(enumerate(s1,start=1))
		slot2=dict(enumerate(s2,start=11))
	d={'slot1':slot1.items(),'slot2':slot2.items(),'gate':gate,'slotcheck':1}
	return render(request, 'parking/slots.html', d)

#Create customer profile 
def createCustomer(request):
	if request.user.is_customer==False:
		return redirect('food:logout')
	form = CustomerForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		return redirect("food:restuarant")
	context={
	'form':form,
	'title':"Complete Your profile"
	}
	return render(request,'webapp/profile_form.html',context)

#  Update customer detail
@login_required(login_url='food:index')
def updateCustomer(request,id):
	if request.user.is_customer==False:
		return redirect('parking:logout')
	form  	 = CustomerForm(request.POST or None,instance=request.user.customer)
	if form.is_valid():
		form.save()
		return redirect('food:profile')
	context={
	'form':form,
	'title':"Update Your profile"
	}
	return render(request,'webapp/profile_form.html',context)

@csrf_exempt
@login_required(login_url='food:login')
def restuarantMenu(request,pk=None):
	if request.user.is_customer==False:
		return redirect('food:logout')

	menu = Menu.objects.filter(r_id=pk)
	rest = Restaurant.objects.filter(id=pk)

	items =[]
	for i in menu:
		item = Item.objects.filter(fname=i.item_id)
		for content in item:
			
			temp=[]
			temp.append(content.fname)
			temp.append(content.category)
			temp.append(i.price)
			temp.append(i.id)
			temp.append(rest[0].status)
			temp.append(i.quantity)
			temp.append(content.img)
			items.append(temp)
	context = {
		'items'	: items,
		'rid' 	: pk,
		'rname'	: rest[0].rname,
		# 'rmin'	: rest[0].min_ord,
		'rinfo' : rest[0].info,
		'rlocation':rest[0].location,
	}
	return render(request,'webapp/menu.html',context)

@login_required(login_url='/login/user/')
def checkout(request):
	if request.user.is_customer==False:
		return redirect('food:logout')
	if request.POST:
		addr  = request.POST['address']
		ordid = request.POST['oid']
		Order.objects.filter(id=int(ordid)).update(delivery_addr = addr,
                                                    status=Order.ORDER_STATE_PLACED)
		global order_id_for_otp
		order_id_for_otp=ordid
		return redirect('food:oderplaced')
	else:	
		cart = request.COOKIES['cart'].split(",")
		cart = dict(Counter(cart))
		items = []
		totalprice = 0
		uid = User.objects.filter(username=request.user)
		oid = Order()
		oid.orderedBy = uid[0]
		for x,y in cart.items():
			item = []
			it = Menu.objects.filter(id=int(x))
			if len(it):
				oiid=orderItem()
				oiid.item_id=it[0]
				oiid.quantity=int(y)
				oid.r_id=it[0].r_id
				oid.secret_code=generateOTP()
				oid.save()
				oiid.ord_id =oid
				oiid.save()
				totalprice += int(y)*it[0].price
				item.append(it[0].item_id.fname)
				it[0].quantity = it[0].quantity - y
				it[0].save()
				item.append(y)
				item.append(it[0].price*int(y))
			
			items.append(item)
		oid.total_amount=totalprice
		oid.save()
		context={
			"items":items,
			"totalprice":totalprice,
			"oid":oid.id
		}	
		return render(request,'webapp/order.html',context)

#to generate otp to verify the
def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP

#Order listiing  for users order of users and its status
@login_required(login_url='food:login')
def custorder(request):
	if request.user.is_customer==False:
		return redirect('food:logout')
	if request.method=="POST":
		feed = request.POST['remark']
		orderid = int(request.POST['orderid'])
		rating=int(request.POST['rating'])
		if feed=='':
			feed=None
		p=Order.objects.get(id=orderid)
		
		usr=request.user
		remark=Feedback(customer=usr,remarks=feed,rating=rating,orderid=p)
		remark.save()
	orders = Order.objects.filter(orderedBy=request.user.id).order_by('-timestamp')
	corders = []

	for order in orders:

		user = User.objects.filter(id=order.r_id.user.id)
		user = user[0]
		corder = []
		if user.is_restaurant:
			corder.append(user.restaurant.rname)
			corder.append(user.restaurant.info)
		else:
			corder.append(user.customer.f_name)
			corder.append(user.customer.phone)
		items_list = orderItem.objects.filter(ord_id=order)

		items = []
		for item in items_list:
			citem = []
			citem.append(item.item_id)
			citem.append(item.quantity)
			menu = Menu.objects.filter(id=item.item_id.id)
			citem.append(menu[0].price*item.quantity)
			menu = 0
			items.append(citem)

		corder.append(items)
		corder.append(order.total_amount)
		corder.append(order.id)
		print(order.id)
		

		x = order.status
		if x == Order.ORDER_STATE_WAITING:
		    continue
		elif x == Order.ORDER_STATE_PLACED:
		    x = 1
		elif x == Order.ORDER_STATE_ACKNOWLEDGED:
			x = 2
		elif x == Order.ORDER_STATE_COMPLETED:
			x = 3
		elif x == Order.ORDER_STATE_DISPATCHED:
			x = 4
		elif x == Order.ORDER_STATE_CANCELLED:
			x = 5
		else:
			continue

		corder.append(x)
		corder.append(order.timestamp)
		corder.append(order.delivery_addr)
		corder.append(order.secret_code)
		corders.append(corder)
	print(corders)
	
	context = {
		"orders" : corders,
		
	}

	return render(request,"webapp/custorder.html",context)

####### ------------------- Restaurant Side ------------------- #####

# creating restuarant account
def restRegister(request):
	form =RestuarantSignUpForm(request.POST or None)
	if form.is_valid():
		user      = form.save(commit=False)
		username  =	form.cleaned_data['username']
		password  = form.cleaned_data['password']
		user.is_restaurant=True
		user.set_password(password)
		user.save()
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("food:rcreate")
	context ={
		'form':form
	}			
	return render(request,'webapp/restsignup.html',context)	

# restuarant login
def restLogin(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user     = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active and user.is_restaurant:
				login(request,user)
				return redirect("food:rprofile")
			
			else:
				return render(request,'webapp/restlogin.html',{'error_message':'Your account disable or You are not permitted'})
		else:
			return render(request,'webapp/restlogin.html',{'error_message': 'Invalid Login'})
	return render(request,'webapp/restlogin.html')

# restaurant profile view
@login_required(login_url='/login/restaurant/')
def restaurantProfile(request,pk=None):
	if request.user.is_restaurant==False:
		return redirect('food:logout')
	if pk:
		user = User.objects.get(pk=pk)
	else:
		user=request.user
	
	return render(request,'webapp/rest_profile.html',{'user':user})

# create restaurant detail
@login_required(login_url='/login/restaurant/')
def createRestaurant(request):
	if request.user.is_restaurant==False:
		return redirect('food:logout')
	form=RestuarantForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		return redirect("food:rprofile")
	context={
	'form':form,
	'title':"Complete Your Restaurant profile"
	}
	return render(request,'webapp/rest_profile_form.html',context)

#Update restaurant detail
@login_required(login_url='/login/restaurant/')
def updateRestaurant(request,id):
	if request.user.is_restaurant==False :
		return redirect('food:logout')
	form  	 = RestuarantForm(request.POST or None,request.FILES or None,instance=request.user.restaurant)
	if form.is_valid():
		form.save()
		return redirect('food:rprofile')
	context={
	'form':form,
	'title':"Update Your Restaurant profile"
	}
	return render(request,'webapp/rest_profile_form.html',context)

#add item for MENU by restaurants
@login_required(login_url='/login/restaurant/')
def additem(request):
	if request.user.is_restaurant==False:
		return redirect('food:logout')
	err=False
	if not request.user.is_authenticated:
		return redirect("food:rlogin") 
	if request.POST:
		form = itemadd(request.POST, request.FILES)
		if form.is_valid():
			obj=form.save(commit=False)
			data = form.cleaned_data
			field = data['fname']
			it=Item.objects.filter(fname=field,rid=request.user.restaurant.id)
			if it.count()==0:
				obj.rid=request.user.restaurant.id
				obj.save()
			else:
				err=True
		# rest=Restaurant.objects.filter(id=request.user.restaurant.id);
		# rest=rest[0]
		# rid=(request.user.restaurant.id)
		# type=request.POST['submit']
		# it = (request.POST['iname'])
		# cat	 = (request.POST['cat'])
		# item=Item()
		# item.fname=it
		# item.category=cat
		# item.rid=rid
		# try:
		# 	item.save()
		# except:
		# 	err=False
		# if err:
		# 	return redirect('food:mmenu')
	else:
		form=itemadd()      		
	return render(request,'webapp/additem.html',{'form' : form,'space':err})

# add  menu item for restaurant	
@login_required(login_url='/login/restaurant/')		
def menuManipulation(request):
	if request.user.is_restaurant==False:
		return redirect('food:logout')
	if not request.user.is_authenticated:
		return redirect("food:rlogin") 
	err=False
		
	rest=Restaurant.objects.filter(id=request.user.restaurant.id);
	rest=rest[0]
	rid=request.user.restaurant.id
	if request.POST:
		type=request.POST['submit']
		if type =="Modify":
			menuid = int(request.POST['menuid'])
			memu= Menu.objects.filter(id=menuid).\
					update(price=int(request.POST['price']),quantity=int(request.POST['quantity']))
		elif type == "Add" :
			itemid=int(request.POST['item'])
			item=Item.objects.filter(id=itemid)
			item=item[0]
			M=Menu.objects.filter(item_id=item)
			if M.count()==0:
				menu=Menu()
				menu.item_id=item
				menu.r_id=rest
				menu.price=int(request.POST['price'])
				menu.quantity=int(request.POST['quantity'])
				menu.save()
			else:
				err=True
		else:
			menuid = int(request.POST['menuid'])
			menu = Menu.objects.filter(id=menuid)
			menu[0].delete()

	menuitems=Menu.objects.filter(r_id=rest)
	menu=[]
	for x in menuitems:
		cmenu=[]
		cmenu.append(x.item_id)
		cmenu.append(x.price)
		cmenu.append(x.quantity)
		cmenu.append(x.id)
		menu.append(cmenu)

	menuitems = Item.objects.filter(rid=request.user.restaurant.id)
	
	items = []
	for y in menuitems:
		print(y)
		citem = []
		citem.append(y.id)
		citem.append(y.fname)
		items.append(citem)

	context={
		"menu":menu,
		"items":items,
		"username":request.user.username,
		"err":err
	}
	return render(request,'webapp/menu_modify.html',context)


@login_required(login_url='/login/restaurant/')	
def orderlist(request):
	if request.user.is_restaurant==False:
		return redirect('food:logout')
	if request.POST:
		oid = request.POST['orderid']
		select = request.POST['orderstatus']
		select = int(select)
		order = Order.objects.filter(id=oid)
		if len(order):
			x = Order.ORDER_STATE_WAITING
			if select == 1:
				x = Order.ORDER_STATE_PLACED
			elif select == 2:
				x = Order.ORDER_STATE_ACKNOWLEDGED
			elif select == 3:
				x = Order.ORDER_STATE_COMPLETED
			elif select == 4:
				x = Order.ORDER_STATE_DISPATCHED
			elif select == 5:
				x = Order.ORDER_STATE_CANCELLED
			else:
				x = Order.ORDER_STATE_WAITING
			order[0].status = x
			order[0].save()

	orders = Order.objects.filter(r_id=request.user.restaurant.id).order_by('-timestamp')
	corders = []

	for order in orders:

		user = User.objects.filter(id=order.orderedBy.id)
		user = user[0]
		print(user.customer.f_name)
		corder = []
		if user.is_restaurant:
			corder.append(user.restaurant.rname)
			corder.append(user.restaurant.info)
		else:
			corder.append(user.customer.f_name)
			corder.append(user.customer.phone)
		items_list = orderItem.objects.filter(ord_id=order)

		items = []
		for item in items_list:
			citem = []
			citem.append(item.item_id)
			citem.append(item.quantity)
			menu = Menu.objects.filter(id=item.item_id.id)
			citem.append(menu[0].price*item.quantity)
			menu = 0
			items.append(citem)
		
		corder.append(items)
		corder.append(order.total_amount)
		corder.append(order.id)

		x = order.status
		if x == Order.ORDER_STATE_WAITING:
		    continue
		elif x == Order.ORDER_STATE_PLACED:
		    x = 1
		elif x == Order.ORDER_STATE_ACKNOWLEDGED:
			x = 2
		elif x == Order.ORDER_STATE_COMPLETED:
			x = 3
		elif x == Order.ORDER_STATE_DISPATCHED:
			x = 4
		elif x == Order.ORDER_STATE_CANCELLED:
			x = 5
		else:
			continue
		print(order.id)
		feed=Feedback.objects.filter(orderid=order.id)
		print(feed.count())
		
		corder.append(x)
		corder.append(order.delivery_addr)
		if feed.count()!=0:
			corder.append(feed[0].rating)
			if feed[0].remarks!=None:
				corder.append(feed[0].remarks)
			else:
				corder.append("No Remark Given")

		else:
			corder.append("NO Rating given")
			corder.append("No Remark Given")
		corders.append(corder)

	context = {
		"orders" : corders,
	}

	return render(request,"webapp/order-list.html",context)

def analytics(request):
	from django.db.models import Count,Sum
	orders = Order.objects.filter(r_id=request.user.restaurant.id)
	no_of_orders=orders.count()
	orderitem=orderItem.objects.filter(ord_id__in=orders).values('item_id').order_by('item_id').annotate(dcount=Sum('quantity')).order_by('-dcount')
	last_week_orders = Order.objects.filter(r_id=request.user.restaurant.id,timestamp__range=last_week())
	no_of_last_week_orders=last_week_orders.count()
	print(orderitem)
	
	max_ordered_item=orderitem[0]
	print(max_ordered_item['item_id'])
	max_ordered_item=Menu.objects.get(id=max_ordered_item['item_id'])
	max_ordered_item=Item.objects.get(fname=max_ordered_item.item_id)
	print(max_ordered_item)



	ordered_item_last_week=orderItem.objects.filter(ord_id__in=last_week_orders).values('item_id').order_by('item_id').annotate(dcount=Sum('quantity')).order_by('-dcount')
	max_ordered_item_last_week=ordered_item_last_week[0]
	max_ordered_item_last_week=Menu.objects.get(id=max_ordered_item_last_week['item_id'])
	max_ordered_item_last_week=Item.objects.get(fname=max_ordered_item_last_week.item_id)
	Total_revenue=0
	for i in orderitem:
	
		price=Menu.objects.get(id=i['item_id'])
		Total_revenue=Total_revenue + price.price*i['dcount']


	context={
		'totalorders':no_of_orders,
		'weekorders':no_of_last_week_orders,
		'maxordereditem':max_ordered_item,
		'maxitemcount':orderitem[0]['dcount'],
		'maxorderlastweek':max_ordered_item_last_week,
		'lastweekitemcount':ordered_item_last_week[0]['dcount'],
		'total_revenue':Total_revenue,
		'items':orderitem

	}
	return render(request,'webapp/analytics.html',context)
import datetime
def last_week():
    today = datetime.date.today()
    return [
        today - datetime.timedelta(days=7),
        today - datetime.timedelta(days=0)
    ]	

	
	
	
	
	



