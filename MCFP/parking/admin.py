from django.contrib import admin
from .models import Category,Vehicle,parking_slots

# Register your models here.


# class slot(admin.ModelAdmin):
#     def get_queryset(self, request):
#         return self.model.objects.filter(is_gate = True)

#     list_filter=('User',get_queryset,)

admin.site.register(Category)
admin.site.register(Vehicle)
admin.site.register(parking_slots)
