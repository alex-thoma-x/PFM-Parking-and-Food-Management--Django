from django.contrib import admin
from .models import Category,Vehicle,parking_slots


# Register your models here.


# class slot(admin.ModelAdmin):
#     def get_queryset(self, request):
#         return self.model.objects.filter(is_gate = True)

#     list_filter=('User',get_queryset,)

class park(admin.ModelAdmin):
    list_display = (
        'user', 'Total_Slots', 'parked',
        )

class vehicle(admin.ModelAdmin):
    list_filter = ['status','gate']
    search_fields = ['regno','ownercontact']
    list_display = (
        'regno', 'pdate', 'ownercontact','status','gate','slot'
        )

admin.site.register(Category)
admin.site.register(Vehicle,vehicle)
admin.site.register(parking_slots,park)
