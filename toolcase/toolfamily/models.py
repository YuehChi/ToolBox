from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import (
#  BaseUserManager, AbstractBaseUser
# )
"""
筆記：
- unique 表示是否要求值必須是唯一的
- default 表示預設的填入值
- blank=True 表示允許創建時給定空值
- null=True 表示允許此項為空值(字串欄位的空值為空字串，其他欄位則是真的空值)
- verbose_name 表示此項目顯示於後台的名稱
- __str__(self) 應回傳字串，表示這個 class 拿去 print() 時會顯示什麼
"""


# Create your models here.

class ToolBoxUser(models.Model):
    account = models.OneToOneField(User, related_name='toolboxAccount', on_delete=models.CASCADE)  # 連接到預設的User帳號
    name = models.CharField(max_length=30, default='', blank=False, verbose_name='全名')
    nickName = models.CharField(max_length=10, default='', blank=True, verbose_name='暱稱')
    selfIntro = models.TextField(default='', blank=True, verbose_name='自我介紹')

    takeTaskPermission = models.BooleanField(default=True, blank=True, null=False, verbose_name='可否應徵當工具人')
    uploadTaskPermission = models.BooleanField(default=True, blank=True, null=False, verbose_name='可否發布委託')

    class Meta:
        verbose_name = '工具人帳號'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.name}({self.nickName})'



# class AccountManager(BaseUserManager):
#     """
#     Custom user model manager where email is the unique identifiers
#     for authentication instead of usernames.
#     """
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a User with the given email and password.
#         """
#         if not email:
#             raise ValueError(_('The Email must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#         return self.create_user(email, password, **extra_fields)



# class Account(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=30, default='', blank=False, null=False, verbose_name='全名')
#     nickName = models.CharField(max_length=10, default='', blank=True, null=True, verbose_name='暱稱')
#     selfIntro = models.TextField(default='', blank=True, null=True, verbose_name='自我介紹')

#     canTakeTask = models.BooleanField(default=True, blank=True, null=True,verbose_name='可否應徵當工具人')
#     canUploadTask = models.BooleanField(default=True, blank=True, null=True, verbose_name='可否發布委託')
#     is_superuser = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)

#     objects = AccountManager()  # 使用哪個 model manager
#     USERNAME_FIELD = 'email'  # 視為帳號名稱的部分
#     REQUIRED_FIELDS = ['name']  # 必須填寫的部分

#     def __str__(self):
#         return self.email

#     def is_admin(self):
#         return self.is_admin
