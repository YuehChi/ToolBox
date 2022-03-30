from django import forms
from .models import *



# 更改使用者基本資料
class UserDetailModelForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = (  # 可以改那些欄位
            'name',  # 本名在這裡設置成可以改
            'nickname',
            'account_mail',
            'gender',
            'department',
            'work',
            'contact',
            'information',
            'icon',
            )
