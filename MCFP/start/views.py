from django.shortcuts import render, HttpResponse
from django.contrib.auth import login, logout, authenticate
from .models import User
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
        elif user.is_cctv:
            rle=2
        elif user.is_restaurant:
            return redirect('food:mmenu')
        elif user.is_customer:
            return redirect('food:restaurant')
        else:
            return render(request, 'home/adindex.html')
        print(error)
    d = {'error': error,'role':rle}
    return render(request, 'home/login.html', d)