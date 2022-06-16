from django.db.models import Q
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta, time
import random
from django.contrib.auth.decorators import login_required
from start.models import User
# Create your views here.

def Index(request):
    return render(request, 'parking/index.html')


def about(request):
    return render(request, 'parking/about.html')


def contact(request):
    return render(request, 'parking/contact.html')


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        rle=0
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
            
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'parking/admin_login.html', d)

@login_required(login_url='home:login')
def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if request.user.is_gate==False and request.user.is_superuser==False:
        return redirect('parking:logout')
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    lasts = today - timedelta(7)

    tv = Vehicle.objects.filter(pdate=today).count()
    yv = Vehicle.objects.filter(pdate=yesterday,gate=request.user.username).count()
    g = Vehicle.objects.filter(pdate=today, gate=request.user.username).count()
    ls = Vehicle.objects.filter(pdate__gte=lasts, pdate__lte=today,gate=request.user.username).count()
    totalv = Vehicle.objects.all().count()

    d = {'tv': tv, 'yv': yv, 'ls': ls, 'totalv': totalv, 'g': g}
    return render(request, 'parking/admin_home.html', d)


def Logout(request):
    logout(request)
    return redirect('parking:index')

@login_required(login_url='home:login')
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
        
    error = ""
    if request.method == "POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'parking/change_password.html', d)

@login_required(login_url='home:login')
def add_category(request):
   
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    error = ""
    exist=1
    if request.method == "POST":
        cn = request.POST['categoryname'].lower()
        p=Category.objects.filter(categoryname=cn).count()
        if p>0:
            exist=0
        else:
            try:
                Category.objects.create(categoryname=cn)
                error = "no"
            except:
                error = "yes"
    d = {'error': error,'exist':exist}
    return render(request, 'parking/add_category.html', d)

@login_required(login_url='home:login')
def manage_category(request):
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    category = Category.objects.all()
    d = {'category': category}
    return render(request, 'parking/manage_category.html', d)

@login_required(login_url='home:login')
def delete_category(request, pid):
    
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('parking:manage_category')

@login_required(login_url='home:login')
def edit_category(request, pid):
    
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    category = Category.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        cn = request.POST['categoryname']
        category.categoryname = cn
        try:
            category.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error, 'category': category}
    return render(request, 'parking/edit_category.html', d)

@login_required(login_url='home:login')
def add_vehicle(request):
    
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    error = ""
    exist=1
    category1 = Category.objects.all()
    if request.method == "POST":

        usr = request.user.username
        import time
        t = time.localtime()
        current_time = time.strftime("%H:%M", t)

        ct = request.POST['category']
        rn = request.POST['regno']
        oc = request.POST['ownercontact']
        it = current_time

        import datetime
        i = datetime.date.today()

        status = "In"
        category = Category.objects.get(categoryname=ct)
        vehicle = Vehicle.objects.filter(regno=rn,status="In")
        if vehicle.count() != 0:
            exist = 0
        else:
            try:
                Vehicle.objects.create(category=category, regno=rn, ownercontact=oc, pdate=i, intime=it, outtime='',
                                    parkingcharge='', status=status, gate=usr)
                error = "no"
            except:
                error = "yes"
    d = {'error': error, 'category1': category1,'exist':exist}
    return render(request, 'parking/add_vehicle.html', d)


def manage_incomingvehicle(request):
    
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    vehicle = Vehicle.objects.filter(status="In")
    d = {'vehicle': vehicle}
    return render(request, 'parking/manage_incomingvehicle.html', d)

@login_required(login_url='home:login')
def view_incomingdetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('parking:admin_home')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    error = ""
    vehicle = Vehicle.objects.get(id=pid)
    if request.method == 'POST':
        rm = request.POST['remark']
        # import datetime
        # i = datetime.date.today()
        import time


        t = time.localtime()
        out_time = time.strftime("%H:%M %d/%m/%y")
        current_time = datetime.strptime(time.strftime("%H:%M", t),"%H:%M")
        v1=datetime.strptime(vehicle.pdate.strftime("%d/%m/%y"),"%d/%m/%y" )
        v2=datetime.strptime(datetime.now().strftime("%d/%m/%y"),"%d/%m/%y" )
        print(1 if v1==v2 else 0)
        if(v1==v2):
            p=current_time-datetime.strptime(vehicle.intime,"%H:%M")
            print("*************************************************")
        else:
            p=(v2-v1)
            print(p)
            p=p+current_time-datetime.strptime(vehicle.intime,"%H:%M")
        pc =((p.total_seconds()%3600)// 60)*10
        status = "Out"
        try:
            vehicle.remark = rm
            vehicle.outtime = out_time
            vehicle.parkingcharge = pc
            vehicle.status = status
            vehicle.save()
            error = "no"
        except:
            error = "yes"

    d = {'vehicle': vehicle, 'error': error}
    return render(request, 'parking/view_incomingdetail.html', d)

@login_required(login_url='home:login')
def manage_outgoingvehicle(request):
    
    if not request.user.is_authenticated:
        return redirect('parkimg:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    vehicle = Vehicle.objects.filter(status="Out")
    d = {'vehicle': vehicle}
    return render(request, 'parking/manage_outgoingvehicle.html', d)

@login_required(login_url='home:login')
def view_outgoingdetail(request, pid):
   
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    vehicle = Vehicle.objects.get(id=pid)

    d = {'vehicle': vehicle}
    return render(request, 'parking/view_outgoingdetail.html', d)

@login_required(login_url='home:login')
def print_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    vehicle = Vehicle.objects.get(id=pid)

    d = {'vehicle': vehicle}
    return render(request, 'parking/print.html', d)

@login_required(login_url='home:login')
def search(request):
    if request.user.is_gate==False:
        return redirect('parking:logout')
    q = None
    vehiclecount=0
    if request.method == 'POST':
        q = request.POST['searchdata']
    try:
        vehicle = Vehicle.objects.filter(Q(regno__contains=q))
        vehiclecount = vehicle.count()

    except:
        vehicle = ""
    d = {'vehicle': vehicle, 'q': q, 'vehiclecount': vehiclecount}
    return render(request, 'parking/search.html', d)
@login_required(login_url='home:login')
def betweendate_reportdetails(request):
    
    if not request.user.is_authenticated:
        return redirect('parking:index')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    return render(request, 'parking/betweendate_reportdetails.html')

@login_required(login_url='home:login')
def betweendate_report(request):
    
    if not request.user.is_authenticated:
        return redirect('parking:index')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        vehicle = Vehicle.objects.filter(Q(pdate__gte=fd) & Q(pdate__lte=td))
        vehiclecount = Vehicle.objects.filter(Q(pdate__gte=fd) & Q(pdate__lte=td)).count()
        d = {'vehicle': vehicle, 'fd': fd, 'td': td, 'vehiclecount': vehiclecount}
        return render(request, 'parking/betweendate_reportdetails.html', d)
    return render(request, 'parking/betweendate_report.html')
