from django.urls import path
from . import views
from start import views as v
from django.conf import settings
from django.conf.urls.static import static

app_name='parking'


urlpatterns = [
path('',v.homelogin,name='index'),
path('about',views.about,name='about'),
path('contact',views.contact,name='contact'),
path('admin_login',v.homelogin,name='admin_login'),
path('admin_home',views.admin_home,name='admin_home'),
path('slot',views.parkslot,name='parkslot'),
path('logout',views.Logout,name='logout'),
path('change_password',views.change_password,name='change_password'),
path('add_category',views.add_category,name='add_category'),
path('manage_category',views.manage_category,name='manage_category'),
path('delete_category/<int:pid>', views.delete_category,name='delete_category'),
path('edit_category/<int:pid>',views.edit_category,name='edit_category'),
path('add_vehicle',views.add_vehicle,name='add_vehicle'),
path('manage_incomingvehicle',views.manage_incomingvehicle,name='manage_incomingvehicle'),
path('view_incomingdetail/<int:pid>',views.view_incomingdetail,name='view_incomingdetail'),
path('manage_outgoingvehicle',views.manage_outgoingvehicle,name='manage_outgoingvehicle'),
path('view_outgoingdetail/<int:pid>',views.view_outgoingdetail,name='view_outgoingdetail'),
path('print/<int:pid>',views.print_detail,name='print'),
path('search',views.search,name='search'),
path('betweendate_report',views.betweendate_report,name='betweendate_report'),
path('betweendate_reportdetails',views.betweendate_reportdetails,name='betweendate_reportdetails'),
]
# urlpatterns = [
#     path('',views.Landingpage,name="landing"),
#     path('register',views.Register,name="Register"),
#     path('login',views.Login,name="Login"),
#     path('logout',views.Logout,name='logout')
# ]