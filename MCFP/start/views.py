from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import login, logout, authenticate
from .models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def homelogin(request):
    error = ""
    rle=-1
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        print(u,p)
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"                
            else:
                error = "yes"
                      
            
        except:
            error = "yes"
        if user.is_gate:
            rle=1
       
        elif user.is_restaurant:
            return render(request, 'webapp/order-list.html')
        elif user.is_customer:
            return render(request, 'webapp/restaurents.html')
        else:
            return HttpResponseRedirect(reverse('admin:index'))
        print(error)
    d = {'error': error,'role':rle}
    return render(request, 'home/login.html', d)