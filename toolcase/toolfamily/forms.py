from django import forms
from .models import *



# 更改使用者基本資料
class UserDetailModelForm(forms.ModelForm):
    class Meta:
        # 表單欄位
        model = UserDetail
        fields = (  # 可以改那些欄位
            'name',  # 本名在這裡設置成可以改
            'nickname',
            # 'account_mail',  # 這是帳號名，不可更改
            'gender',
            'department',
            'work',
            'contact',
            'information',
            'icon',
            )

    def clean_account_mail(self, *args, **kwargs):
        email = self.cleaned_data.get('account_mail') #取得樣板所填寫的資料
        if not email.endswith('@ntu.edu.tw'):
            print('email not end with @ntu.edu.tw')
            raise forms.ValidationError('請使用 NTU 電子郵件')
        return email
