from django.contrib import admin
from .models import *



class customer(admin.ModelAdmin):
    search_fields = ['f_name','l_name']
    list_display = (
        'user', 'f_name','l_name', 'phone'
        )
    # def has_delete_permission(self, request, obj=None):
    #     return False
class restaurant(admin.ModelAdmin):
    search_fields = ['rname','info']
    list_display = (
        'user', 'rname','info', 'location'
        )
    # def has_delete_permission(self, request, obj=None):
    #     return False

class item(admin.ModelAdmin):
    list_filter = ['category']
    list_display = (
        'fname', 'category'
        )
    # def has_delete_permission(self, request, obj=None):
    #     return False

class menu(admin.ModelAdmin):
    list_filter = ['r_id','item_id']
    list_display = (
        'r_id', 'item_id','price','quantity'
        )
    

class order(admin.ModelAdmin):
    list_filter = ['status']
    list_display = (
        'orderedBy', 'delivery_addr','timestamp','r_id','total_amount','status'
        )
    # def has_delete_permission(self, request, obj=None):
    #     return False

admin.site.register(Customer,customer)
admin.site.register(Restaurant,restaurant)
admin.site.register(Item,item)
admin.site.register(Menu,menu)
admin.site.register(Order,order)
admin.site.register(Feedback)
# admin.site.register(orderItem)