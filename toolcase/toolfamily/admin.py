from django.contrib import admin
from .models import *

# Register your models here.


class ToolBoxUserAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        '__str__',
        'account',
        'takeTaskPermission',
        'uploadTaskPermission',
    )
admin.site.register(ToolBoxUser, ToolBoxUserAdmin)


# admin.site.register(Account)
