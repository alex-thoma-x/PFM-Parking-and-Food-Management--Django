from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User

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
admin.site.register(User,CustomUserAdmin)