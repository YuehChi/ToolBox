from django.contrib import admin
from .models import *

# Register your models here.


class UserDetailAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        '__str__',
        'account_mail',
        'gender',
        'department',
        'rate',
        'created_datetime'
    )
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
        'status',
        'shown_public'
    )
admin.site.register(Case, CaseAdmin)



class CaseWillingnessAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'casewillingness_id',
        'case',
        'created_datetime'
    )
admin.site.register(CaseWillingness, CaseWillingnessAdmin)



class CommissionRecordAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'commissionrecord_id',
        'case',
        'commissioned_user',
        'status',
        'rate_toolman',
        'rate_case_publisher',
        'created_datetime',
        'finish_datetime'
    )
admin.site.register(CommissionRecord)



class ReportAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'report_id',
        'report_type',
        'reporter',
        'reported_case',
        'reported_user',
        'status',
        'confirmed'
    )
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
