from django.contrib import admin
from polls.models import Equipment, Data


class EquipmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('设备名', {'fields': ['name']}),
        ('描述', {'fields': ['descript']}),
        ('key', {'fields': ['key']}),
    ]


admin.site.register(Equipment, EquipmentAdmin)
