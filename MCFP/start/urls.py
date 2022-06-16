from django.urls import path
from.import views
from parking import views as v
from django.contrib.auth import views as auth_views

app_name='home'

urlpatterns = [
    path("",v.Index,name='home'),
    path("login/",views.homelogin,name='login')
   ]