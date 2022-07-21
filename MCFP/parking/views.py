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
import random
import pytz
from datetime import  timedelta,timezone
from dateutil.tz import gettz
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
            if user.is_staff and user.is_gate:
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
    if request.user.is_gate==False:
        return redirect('parking:logout')
    today = datetime.now().date()
    
    yesterday = today - timedelta(1)
    yesterday_max=datetime.combine(yesterday, time.max)
    lasts = today - timedelta(7)

    s=parking_slots.objects.filter(user=request.user.id)
    for i in s:
        slots=i.Total_Slots-i.parked
    print(slots)     
    tv = Vehicle.objects.filter(pdate__date__range=(today, datetime.now(pytz.timezone('Indian/Mahe')))).count()
    yv = Vehicle.objects.filter(pdate__date__range=(yesterday,yesterday_max),gate=request.user.username).count()
    g = Vehicle.objects.filter(pdate__date__range=(today, datetime.now(pytz.timezone('Indian/Mahe'))), gate=request.user.username).count()
    ls = Vehicle.objects.filter(pdate__gte=lasts, pdate__lte=today,gate=request.user.username).count()
    totalv = Vehicle.objects.all().count()

    usr=request.user.username
    slot_set=slotcheck(usr)
    print(slot_set)
    slot=[False]*20
    for i in range(20):
        if i+1 in slot_set:
            slot[i]=True
    s1=slot[:10]
    s2=slot[10:]
    slot1 = dict(enumerate(s1,start=1))

    slot2=dict(enumerate(s2,start=11))
   
       
    d = {'tv': tv, 'yv': yv, 'ls': ls, 'totalv': totalv, 'g': g,'slots':slots,'slot1':slot1.items(),'slot2':slot2.items()}
    return render(request, 'parking/admin_home.html', d)


def Logout(request):
    logout(request)
    return redirect('home:staff')

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

def slotcheck(usr):
    for record in Booking.objects.all():
        time_elapsed = datetime.now(tz=gettz('Asia/Kolkata')) - record.time
        if time_elapsed > timedelta(hours=1):
            record.delete()
    slot_check_list=[i for i in range(1,21)]
    slot_check_set=set(slot_check_list)
    slot_value_db=Vehicle.objects.filter(status='In',gate=usr)
    for i in slot_value_db:
        if i.slot in slot_check_set:
            slot_check_set.remove(i.slot)
    slot_value_db=Booking.objects.filter(gate=usr)
    for i in slot_value_db:
        if i.slot in slot_check_set:
            slot_check_set.remove(i.slot)


    return slot_check_set

@login_required(login_url='home:login')
def parkslot(request):
    usr=request.user.username
    slot_set=slotcheck(usr)
    print(slot_set)
    slot=[False]*20
    for i in range(20):
        if i+1 in slot_set:
            slot[i]=True
    s1=slot[:10]
    s2=slot[10:]
    slot1 = dict(enumerate(s1,start=1))
    slot2=dict(enumerate(s2,start=11))
   
    print(slot1,slot2)
    d={'slot1':slot1.items(),'slot2':slot2.items()}
    return render(request, 'parking/slots.html', d)
    

@login_required(login_url='home:login')
def add_vehicle(request):        
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    error = ""
    exist=1
    space=False
    mob=False
    s=parking_slots.objects.filter(user=request.user.id)
    for i in s:
        slot=i.Total_Slots-i.parked
    print(slot)
    category1 = Category.objects.all()
    if request.method == "POST":
        if slot!=0:
            usr = request.user.username
            slot_check_set=slotcheck(usr)
            
            free_slot= min(slot_check_set) #random.choice(tuple(slot_check_set))                   

            import time
            t = time.localtime()
            current_time = time.strftime("%H:%M", t)

            ct = request.POST['category']
            rn = request.POST['regno']
            oc = request.POST['ownercontact']
            it = current_time
            book=Booking.objects.filter(mobile=oc)
            if book.count()>0:
                free_slot=book[0].slot
                book[0].delete()
            slt=free_slot
            
            
            import datetime
            i = datetime.datetime.now(pytz.timezone('Indian/Mahe'))
            

            status = "In"
            category = Category.objects.get(categoryname=ct)
            vehicle = Vehicle.objects.filter(regno=rn,status="In")
            mobile=Vehicle.objects.filter(ownercontact=oc,status="In")

            if vehicle.count() != 0:
                exist = 0
            elif mobile.count()!=0:
                mob=True                
            else:
                try:
                    Vehicle.objects.create(category=category, regno=rn, ownercontact=oc, pdate=i, intime=it, outtime='',
                                        parkingcharge='', status=status, gate=usr, slot=slt)
                    for i in s:
                        slot=i.Total_Slots-i.parked
                        add_slot=i.parked+1
                        i.parked=add_slot
                        i.save()
                    error = "no"
                except:
                    error = "yes"
        else:
            space=True
    d = {'error': error, 'category1': category1,'exist':exist,'space':space,'mob':mob}
    return render(request, 'parking/add_vehicle.html', d)


def manage_incomingvehicle(request):
    
    if not request.user.is_authenticated:
        return redirect('parking:admin_login')
    if request.user.is_gate==False:
        return redirect('parking:logout')
    vehicle = Vehicle.objects.filter(status="In",gate=request.user.username)
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
            #Price setting-----------------------------------------------------------------------
        pc =((p.total_seconds()%3600)// 60)*10
        status = "Out"
        s=parking_slots.objects.filter(user=request.user.id)
        
        try:
            
            vehicle.remark = rm
            vehicle.outtime = out_time
            vehicle.parkingcharge = pc
            vehicle.status = status
            vehicle.save()
            error = "no"
        except:
            error = "yes"
        for i in s:
            i.parked=i.parked-1
            i.save()

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
