from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        )
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                )
        }),
        # ('Important dates', {
        #     'fields': ('last_login', 'date_joined')
        # }),
        ('Role', {
            'fields': ( 'is_customer','is_gate','is_cctv','is_restaurant')
        })
    )
    def has_delete_permission(self, request, obj=None):
        return False

    # def get_queryset(self, request):
    #     return self.model.objects.filter(is_gate = True)


class Myuser(CustomUserAdmin):
    list_display = (
        'username',
        )
    def get_queryset(self, request):
        return self.model.objects.filter(is_gate = True)
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        
        ('Role', {
            'fields': ( 'is_gate',)
        })
    )
    def has_delete_permission(self, request, obj=None):
        return False
from django.contrib.auth.models import Group

admin.site.unregister(Group)




admin.site.register(User,CustomUserAdmin)
admin.site.register(gatekeepers,Myuser)