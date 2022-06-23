from django.contrib import admin
from .models import Customer,Restaurant,Item,Menu,Order,orderItem,User


class customer(admin.ModelAdmin):
    search_fields = ['f_name']
    list_display = (
        'user', 'f_name','l_name', 'phone'
        )
class restaurant(admin.ModelAdmin):
    search_fields = ['rname']
    list_display = (
        'user', 'rname','info', 'location'
        )

class item(admin.ModelAdmin):
    list_filter = ['category']
    list_display = (
        'fname', 'category'
        )

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

admin.site.register(Customer,customer)
admin.site.register(Restaurant,restaurant)
admin.site.register(Item,item)
admin.site.register(Menu,menu)
admin.site.register(Order,order)
# admin.site.register(orderItem)