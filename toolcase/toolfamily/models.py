from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import (
#  BaseUserManager, AbstractBaseUser
# )

import datetime

"""
筆記：
- unique 表示是否要求值必須是唯一的
- default 表示預設的填入值
- blank=True 表示允許創建時給定空值
- null=True 表示允許此項為空值(字串欄位的空值為空字串，其他欄位則是真的空值)
- verbose_name 表示此項目顯示於後台的名稱
- __str__(self) 應回傳字串，表示這個 class 拿去 print() 時會顯示什麼

DB內的刪除怎麼處理
- 若委託人/工具人刪帳號，委託單與委託紀錄不會消失（僅是將委託/接案者設為 null）
  - 應該是不讓刪，只准許改為停用的帳號更好
"""


# Create your models here.



# 完整的使用者帳號
class ToolBoxUser(models.Model):
    account = models.OneToOneField(User, related_name='toolboxAccount', on_delete=models.CASCADE)  # 連接到預設的User帳號
    name = models.CharField(max_length=30, default='', blank=False, verbose_name='全名')
    nickName = models.CharField(max_length=10, default='', blank=True, verbose_name='暱稱')
    selfIntro = models.TextField(default='', blank=True, verbose_name='自我介紹')

    takeTaskPermission = models.BooleanField(default=True, verbose_name='可否應徵當工具人')
    uploadTaskPermission = models.BooleanField(default=True, verbose_name='可否發布委託')
    isActive = models.BooleanField(default=True, verbose_name='啟用狀態')
    createAt = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')

    class Meta:
        verbose_name = '帳號'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.name}({self.nickName})'



# 委託單狀態
class TaskState(models.Model):
    name = models.CharField(max_length=10, default='-', verbose_name='狀態名稱')
    description = models.CharField(max_length=30, default='', verbose_name='說明')

    class Meta:
        verbose_name = '委託單狀態'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.name}'



# 委託單
class Task(models.Model):
    # 要給人看的
    title = models.CharField(max_length=30, default='', blank=False, verbose_name='標題')
    description = models.TextField(default='', blank=True, verbose_name='描述')
    reward = models.CharField(max_length=30, default='', blank=True, verbose_name='報酬')
    location = models.CharField(max_length=50, default='', blank=True, verbose_name='地點')
    solution = models.CharField(max_length=50, default='', blank=True, verbose_name='解決方法')
    limitation = models.CharField(max_length=50, default='', blank=True, verbose_name='限制條件')
    startTime = models.DateTimeField(default=None, blank=True, null=True,
        verbose_name='開始時間')  # 預計委託開始時間（預設為空）
    endTime = models.DateTimeField(default=None, blank=True, null=True,
        verbose_name='結束時間')  # 預計委託結束時間（預設為空）

    # 類型、領域、標籤屬於 many to many，在其各自的 table 中定義再連結至此

    # 後台的發布、接案、下架、修改紀錄
    # 註：一件委託只有一個委託人，但委託單和應徵者、接案者是 man to many 關係
    creator = models.ForeignKey(ToolBoxUser, related_name='tasks',
        null=True, verbose_name='委託人', on_delete=models.SET_NULL)
    createAt = models.DateTimeField(auto_now_add=True, verbose_name='發布時間')
    assignAt = models.DateTimeField(default=None, blank=True, null=True,
        verbose_name='成案時間', help_text='委託人確定給哪些工具人做的時間點')
    finishAt = models.DateTimeField(default=None, blank=True, null=True,
        verbose_name='完成時間', help_text='工具人按下確定的時間點')
    doubleCheckFinishAt = models.DateTimeField(default=None, blank=True, null=True,
        verbose_name='雙重確認-完成時間', help_text='委託人按下確定的時間點')
    lastChange = models.DateTimeField(auto_now=True, verbose_name='最後修改')
    # 註：「最後修改」是只要DB裡這行重新存檔就算（即使給人看的部分沒動）

    # 委託單狀態
    state = models.ForeignKey(TaskState, related_name='tasks',
        null=True, verbose_name='狀態', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '委託單'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.title} {self.createAt}'



# 應徵委託的資訊
class TaskApply(models.Model):
    applyer = models.ForeignKey(ToolBoxUser, related_name='applys',
        null=True, verbose_name='應徵者', on_delete=models.SET_NULL)
    task = models.ForeignKey(Task, related_name='applys',
        null=True, verbose_name='委託單', on_delete=models.CASCADE)
    text = models.TextField(default='', blank=True, verbose_name='附加資訊')

    createAt = models.DateTimeField(auto_now_add=True, verbose_name='申請時間')
    isAccept = models.BooleanField(default=False, verbose_name='確認接案',
        help_text='當委託人決定委託這人，設為 True')
    isCancel = models.BooleanField(default=False,
        verbose_name='應徵者取消',
        help_text='若應徵者後來要取消，設為 True；可供計算取消次數')

    class Meta:
        verbose_name = '應徵資訊'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.applyer} apply for {self.task}'



# 檢舉
class Report(models.Model):
    reporter = models.ForeignKey(ToolBoxUser, related_name='reports',
        null=True, verbose_name='檢舉人', on_delete=models.SET_NULL)
    reportOnTask = models.ForeignKey(Task, related_name='beReported',  #accused
        null=True, verbose_name='被檢舉的委託單', on_delete=models.SET_NULL)
    reportOnUser = models.ForeignKey(ToolBoxUser, related_name='beReported', #accused
        null=True, verbose_name='被檢舉人', on_delete=models.SET_NULL)
    description = models.TextField(default='', blank=True, verbose_name='描述')
    createAt = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')

    class Meta:
        verbose_name = '檢舉'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.description}'



## class AccountManager and Account are for changing the basic user class.
## not in use because it will cause catalog to fail

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
