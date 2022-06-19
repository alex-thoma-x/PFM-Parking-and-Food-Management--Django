from django.urls import path
from.import views
from webapp import views as w
from parking import views as v
from django.contrib.auth import views as auth_views

app_name='home'

urlpatterns = [
    # path("",v.Index,name='home'),
    path("",w.index,name='index'),
    path("staff", views.homelogin,name='staff')
   ]