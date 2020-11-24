from django.contrib import admin
from polls.models import Equipment, Data


class DataInline(admin.StackedInline):
    model = Data
    extra = 0
    max_num = 20
    fields = ('value', 'descript', 'created_time')
    readonly_fields = ['created_time']


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'descript', 'created_time')
    list_filter = ['created_time']
    fieldsets = [
        ('设备名', {'fields': ['name']}),
        ('描述', {'fields': ['descript']}),
        ('key', {'fields': ['key']}),
        ('created_time', {'fields': ['created_time']}),
    ]
    readonly_fields = ['created_time']
    inlines = [DataInline]


admin.site.register(Equipment, EquipmentAdmin)
