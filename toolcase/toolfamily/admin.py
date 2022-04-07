from django.contrib import admin
from .models import *

# Register your models here.


class UserDetailAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        '__str__',
        'account_mail',
        'gender_shown',
        'department',
        'rate_shown',
        'last_login'
    )
    readonly_fields = (
        'user_id',
        'created_datetime',
        'last_login',
        'work_num',
        'publish_num')
    def gender_shown(self, obj):
        g = obj.gender
        if g == 0:
            return '不願透露'
        elif g == 1:
            return '男'
        elif g == 2:
            return '女'
        else:
            return '其他'
    def rate_shown(self, obj):
        return round(obj.rate, 2)
admin.site.register(UserDetail, UserDetailAdmin)



class CaseAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'case_id',
        'title',
        'publisher',
        'reward',
        'location',
        'ended_datetime',
        'case_status',
        'shown_public'
    )
    readonly_fields = ('created_datetime', 'last_change', 'case_id')
admin.site.register(Case, CaseAdmin)



class CaseWillingnessAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'casewillingness_id',
        'willing_user',
        'apply_case',
        'created_datetime'
    )
    readonly_fields = ('created_datetime', 'casewillingness_id')
admin.site.register(CaseWillingness, CaseWillingnessAdmin)



class CommissionRecordAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'commissionrecord_id',
        'case',
        'commissioned_user',
        'user_status',
        'rate_publisher_to_worker',
        'rate_worker_to_publisher',
        'created_datetime',
        'finish_datetime'
    )
    readonly_fields = ('created_datetime', 'commissionrecord_id')
admin.site.register(CommissionRecord)



class ReportAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'report_id',
        'report_type',
        'reporter',
        'reported_case',
        'reported_user',
        'is_treated',
        'is_valid'
    )
    readonly_fields = ('created_datetime', 'report_id')
admin.site.register(Report, ReportAdmin)



# 這邊是不做處理、直接用預設介面的後台
admin.site.register(Status)
admin.site.register(CasePhoto)
admin.site.register(Type)
admin.site.register(Case_Type)
admin.site.register(Field)
admin.site.register(Case_Field)
admin.site.register(FollowUser)
admin.site.register(FollowCase)
admin.site.register(ReportType)
