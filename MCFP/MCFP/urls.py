
from django.contrib import admin
from django.urls import path
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('food/',include("webapp.urls")),
    path('',include("start.urls")),
    path('parking/',include("parking.urls")),
]
