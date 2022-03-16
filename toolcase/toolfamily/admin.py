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
        'isActive'
    )
admin.site.register(ToolBoxUser, ToolBoxUserAdmin)


class TaskApplyAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'applyer',
        'task',
        'createAt',
        'isAccept',
        'isCancel'
    )
admin.site.register(TaskApply, TaskApplyAdmin)


class TaskAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'title',
        'creator',
        'solution',
        'reward',
        'location',
        'createAt',
    )
admin.site.register(Task, TaskAdmin)


# 這邊是不做處理、直接用預設介面的後台的
admin.site.register(TaskState)


# admin.site.register(Account)
