from django.contrib import admin
from account.models import User, ConfirmString


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('用户名',               {'fields': ['username']}),
        ('邮箱', {'fields': ['email']}),
        ('密码', {'fields': ['password']}),
        ('邮箱确认', {'fields': ['confirmed']}),

    ]


admin.site.register(User, UserAdmin)
admin.site.register(ConfirmString)
