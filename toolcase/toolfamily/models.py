from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import datetime
from uuid import uuid4 as uuid # 為了生成隨機字串


"""
model field 語法筆記
    - unique 表示是否要求值必須是唯一的
    - default 表示預設的填入值
    - blank=True 表示允許輸入空值。請搭配 null=True，否則會很容易出錯。
    - null=True 表示允許此項為空值(字串欄位的空值為空字串，其他欄位則是真的空值)
    - verbose_name 表示此項目顯示於後台的名稱
model 其他項目 筆記
    - def __str__(self) 表示應回傳字串，表示這個 class 拿去 print() 時會顯示什麼
    - class Meta 可以放選擇性的其他設置（可以沒有）
        - verbose_name = '顯示的table名'  表示後台顯示的 table 名稱（和DB中的可以不同）
        - ordering = ['欄位名稱']  表示DB中row按照哪一欄進行排序。
                     先照第一個欄位排序、第一項同則按第二項排序，以此類推。
                     欄位名稱前加'-'表示倒序排列
        - order_with_respect_to = '外鍵名稱'  依據外鍵進行排序

DB內的刪除怎麼處理
    - 若委託人/工具人刪帳號，帳號不會真的刪，只是停用（永久停權同理）
        - 倘若真的刪帳號，委託單與委託紀錄都會一起消失
    - 語法：
        - on_delete=models.CASCADE 外鍵刪除時跟著一起消失
        - on_delete=models.SET_NULL 外鍵刪除時設為空（必須允許是空欄位）
        - on_delete=models.PROTECT 阻止外鍵被刪除
"""


# 生成 n 個字符的隨機字串（目前沒在使用）
def randomStr(n=6):
    randomRef = uuid().hex[:n]
    return randomRef

# 生成作為 primary key 的數字（UUID, 128 bit int）
# 太大了以至於存不進 DB 裡面
def IntUUID():
    randomRef = uuid().int
    return randomRef

# 取得 x 天後的時間
def daysAfter(n=7):
    return timezone.now() + datetime.timedelta(days=n)


#----使用者帳號模組--------------------------------------------------------------

     #    #   ####   ######  #####
     #    #  #       #       #    #
     #    #   ####   #####   #    #
     #    #       #  #       #####
     #    #  #    #  #       #   #
      ####    ####   ######  #    #
#------------------------------------------------------------------------------

# 完整的使用者帳號
class UserDetail(models.Model):
    # ID與安全性
    user_id = models.AutoField(primary_key=True, editable=False)
    django_user = models.OneToOneField(
        User,
        related_name='user_detail',
        on_delete=models.CASCADE)  # 連接到預設的User帳號
    account_mail = models.EmailField(max_length=30,
        unique=True,
        verbose_name='帳號（電子郵件）')
    salt = models.TextField(default=IntUUID,
        verbose_name='隨機雜湊')
    verification = models.BooleanField(
        default=False,
        verbose_name='信箱是否驗證',
        help_text='0:未驗證，1:已驗證')
    created_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='建立時間')

    # 帳號資訊
    name = models.CharField(max_length=10, default='', verbose_name='真實姓名')
    nickname = models.CharField(
        max_length=50,
        default='', blank=True,
        verbose_name='暱稱',
        help_text='主頁上對他人是顯示這個')
    gender = models.IntegerField(
        default=0,
        verbose_name='生理性別',
        help_text='0:不願透露，1:男，2:女，3往後是其他')
    department = models.CharField(
        max_length=30,
        default='', blank=True,
        verbose_name='科系')
    contact = models.TextField(default='',
        verbose_name='聯絡方式',
        help_text='使用者另外填寫的聯絡方式，可以是 line id、messenger 等任意內容')
    information = models.TextField(
        default='', blank=True,
        verbose_name='自我介紹')
    rate = models.DecimalField(
        max_digits=15,
        decimal_places=13,
        default=0,
        null=False, blank=False,
        verbose_name='評價')
    icon = models.ImageField(upload_to='images/userIcon/', null=True, blank=True)

    # 帳號權限
    isActive = models.BooleanField(default=True,
        verbose_name='帳號是否啟用',
        help_text='如果使用者想刪帳號/被永久封號，就把帳號改成停用')

    class Meta:
        verbose_name = '使用者'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.name}({self.nickname})'



# 被舉報紀錄
class UserReportedRecord(models.Model):
    # ID與關連到的使用者
    record_id = models.AutoField(primary_key=True, editable=False)
    reported_user = models.OneToOneField(
        UserDetail,
        related_name='report_record',
        verbose_name='使用者',
        on_delete=models.CASCADE)

    # 停權狀態
    take_expiry_date = models.DateTimeField(
        default=None,
        blank=True, null=True,
        verbose_name='接案停權到期日',
        help_text='若沒有被停權則為空')
    publish_expiry_date = models.DateTimeField(
        default=None,
        blank=True, null=True,
        verbose_name='發布停權到期日',
        help_text='若沒有被停權則為空')
    take_ban_times = models.SmallIntegerField(
        default = 0,
        blank=True, null=True,
        verbose_name='接案停權累積次數',
        help_text='累積達三次則永久停權')
    publish_ban_times = models.SmallIntegerField(
        default = 0,
        blank=True, null=True,
        verbose_name='發布停權累積次數',
        help_text='累積達三次則永久停權')

    class Meta:
        verbose_name = '停權紀錄'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return (f'{self.reported_user} ban times: '
                f'{self.take_ban_times},{publish_ban_times}')



# 追蹤使用者
class FollowUser(models.Model):
    followuser_id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(UserDetail,
        related_name='follow_users',
        verbose_name='跟隨者',
        on_delete=models.CASCADE)
    followed_user = models.ForeignKey(UserDetail,
        related_name='followed_by',
        verbose_name='追蹤的用戶',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = '追蹤使用者'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.user} follows {self.followed_user}.'



# 追蹤委託
class FollowCase(models.Model):
    followcase_id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(UserDetail,
        related_name='follow_cases',
        verbose_name='跟隨者',
        on_delete=models.CASCADE)
    followed_case = models.ForeignKey('Case',  # 這裡用字串是因為Case還沒宣告
        related_name='followed_by',
        verbose_name='追蹤的委託',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = '追蹤委託'  # 給人看的 table 名稱


    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.user} follows {self.followed_case}.'



#----委託模組-------------------------------------------------------------------

      ####     ##     ####   ######
     #    #   #  #   #       #
     #       #    #   ####   #####
     #       ######       #  #
     #    #  #    #  #    #  #
      ####   #    #   ####   ######
#------------------------------------------------------------------------------
# 委託狀態
class Status(models.Model):
    status_id = models.IntegerField(primary_key=True)
    status_name = models.CharField(
        max_length=10,
        default='其他',
        verbose_name='狀態名稱',
        help_text='0:關閉，1:徵求，2:進行，3:完成')

    class Meta:
        verbose_name = '委託狀態'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.status_name}'



# 委託單
class Case(models.Model):
    # ID與發起者
    case_id = models.AutoField(primary_key=True, editable=False)
    publisher = models.ForeignKey(UserDetail,
        related_name='cases',
        verbose_name='委託人', on_delete=models.CASCADE)

    # 委託資訊
    title = models.CharField(max_length=30, default='', blank=False,
        verbose_name='標題')
    description = models.TextField(default='', blank=False,
        verbose_name='內容說明')
    reward = models.CharField(max_length=50, default='', blank=False,
        verbose_name='報酬方式')
    location = models.CharField(max_length=50, default='', blank=True,
        verbose_name='地點')
    constraint = models.CharField(max_length=50, default='', blank=True,
        verbose_name='偏好條件')
    # 類型、領域、標籤屬於 many to many，在其各自的 table 中定義再連結至此

    # 時間
    created_datetime = models.DateTimeField(auto_now_add=True,
        verbose_name='建立時間')
    started_datetime = models.DateTimeField(
        default=None,
        blank=True, null=True,
        verbose_name='開始時間')  # 任務開始時間（預設為空）
    ended_datetime = models.DateTimeField(
        default=daysAfter,
        blank=False, null=False,
        verbose_name='結束時間')  # 任務結束時間（不可為空）
    last_change = models.DateTimeField(auto_now=True,
        verbose_name='最後修改時間')  # 註：只要DB裡這行重新存檔就算

    # 狀態
    pageviews = models.IntegerField(default=0, verbose_name='瀏覽人數')
    case_status = models.ForeignKey(
        Status,
        related_name='case',
        verbose_name='狀態',
        on_delete=models.PROTECT,  # 若有case使用狀態，就不允許刪除狀態
        )
    shown_public = models.BooleanField(
        default=True,
        verbose_name='是否公開顯示',
        help_text='False:不顯示在公開查詢頁面，但已應徵/接案者仍可繼續')

    class Meta:
        verbose_name = '委託單'  # 給人看的 table 名稱
        ordering = ['-created_datetime']


    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.title}'



# 委託單照片
class CasePhoto(models.Model):
    casephoto_id = models.AutoField(primary_key=True, editable=False)
    case = models.ForeignKey(Case,
        related_name='photos',
        verbose_name='委託',
        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/casePhoto/')

    class Meta:
        verbose_name = '委託單照片'  # 給人看的 table 名稱
        order_with_respect_to = 'case'  # 依據外鍵進行排序

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f"{self.case} 的照片"



# 委託類型
class Type(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=10, default='其他',
        blank=False,
        verbose_name='類型名稱')
    case = models.ManyToManyField(Case,
        through='Case_Type',
        through_fields=('case_type', 'case')
        )

    class Meta:
        verbose_name = '委託類型'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return self.type_name


class Case_Type(models.Model):
    casetype_id = models.AutoField(primary_key=True, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    case_type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '委託-類型 關聯表'

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.case}:{self.case_type}'



# 委託領域
class Field(models.Model):
    field_id = models.IntegerField(primary_key=True)
    field_name = models.CharField(max_length=10, default='其他',
        blank=False,
        verbose_name='領域名稱')
    case = models.ManyToManyField(Case,
        through='Case_Field',
        through_fields=('case_field', 'case')
        )

    class Meta:
        verbose_name = '委託領域'  # 給人看的 table 名稱

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return self.field_name


class Case_Field(models.Model):
    casefield_id = models.AutoField(primary_key=True, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    case_field = models.ForeignKey(Field, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '委託-領域 關聯表'

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.case}:{self.case_field}'



#----承接關係模組---------------------------------------------------------------

     #     #                                    #####
     #     #   ####   ######  #####            #     #    ##     ####   ######
     #     #  #       #       #    #           #         #  #   #       #
     #     #   ####   #####   #    #           #        #    #   ####   #####
     #     #       #  #       #####            #        ######       #  #
     #     #  #    #  #       #   #            #     #  #    #  #    #  #
      #####    ####   ######  #    #            #####   #    #   ####   ######
#------------------------------------------------------------------------------
# 承接意願
class CaseWillingness(models.Model):
    # ID與關係人
    casewillingness_id = models.AutoField(primary_key=True, editable=False)
    apply_case = models.ForeignKey(Case,
        related_name='applyed_by',
        verbose_name='委託單',
        on_delete=models.CASCADE)
    willing_user = models.ForeignKey(UserDetail,
        related_name='applys',
        verbose_name='應徵的工具人',
        on_delete=models.CASCADE)

    # 附加資訊
    recommendation = models.TextField(
        default='', blank=True,
        verbose_name='附加資訊')

    # 時間
    created_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='應徵時間')

    class Meta:
        verbose_name = '應徵'  # 給人看的 table 名稱
        order_with_respect_to = 'apply_case'  # 依據外鍵進行排序

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'{self.willing_user} apply for {self.apply_case}'



# 承接關係
class CommissionRecord(models.Model):
    # ID與關係人、關係案件
    commissionrecord_id = models.AutoField(primary_key=True, editable=False)
    case = models.ForeignKey(Case,
        related_name='commission_record',
        verbose_name='委託單',
        on_delete=models.CASCADE)
    commissioned_user = models.ForeignKey(UserDetail,
        related_name='commission_record',
        verbose_name='接案的工具人',
        on_delete=models.CASCADE)
    user_status = models.ForeignKey(Status,
        related_name='commission_record',
        verbose_name='狀態',
        null=True,
        on_delete=models.SET_NULL,
        help_text=('使用者_維修單狀態，'
            '若是工具人身分，則此欄位用於判斷使用者在維修單上的按鈕狀態，'
            '及該維修單在使用者個人頁面狀態'))

    # 評分
    rate_publisher_to_worker = models.SmallIntegerField(
        default=None,
        null=True, blank=True,
        verbose_name='工具人評價',
        help_text='委託人給工具人的評價，整數 1-5')
    rate_worker_to_publisher = models.SmallIntegerField(
        default=None,
        null=True, blank=True,
        verbose_name='委託人評價',
        help_text='工具人給委託人的評價，整數 1-5')

    # 時間
    created_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='成案時間',
        help_text='原則上是委託人確定委託工具人的時間點')
    finish_datetime = models.DateTimeField(
        default=None, blank=True, null=True,
        verbose_name='完成時間',
        help_text='工具人按下確定的時間點')
    doublecheck_datetime = models.DateTimeField(
        default=None, blank=True, null=True,
        verbose_name='雙重確認-完成時間',
        help_text='委託人按下確定的時間點')

    class Meta:
        verbose_name = '承接紀錄'  # 給人看的 table 名稱
        order_with_respect_to = 'case'  # 依據外鍵進行排序

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'({self.user_status}) {self.case}'



#----檢舉模組-------------------------------------------------------------------

     #####   ######  #####    ####   #####   #####
     #    #  #       #    #  #    #  #    #    #
     #    #  #####   #    #  #    #  #    #    #
     #####   #       #####   #    #  #####     #
     #   #   #       #       #    #  #   #     #
     #    #  ######  #        ####   #    #    #
#------------------------------------------------------------------------------

# 檢舉類型
class ReportType(models.Model):
    report_type_id = models.IntegerField(primary_key=True)
    report_type_name = models.CharField(max_length=50,
        blank=False,
        default='其他')

    class Meta:
        verbose_name = '檢舉類型'  # 給人看的 table 名稱
        ordering = ['report_type_id']

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return self.report_type_name



# 檢舉
class Report(models.Model):
    report_id = models.AutoField(primary_key=True, editable=False)

    # 關係人
    reporter = models.ForeignKey(UserDetail,
        related_name='reports',
        verbose_name='檢舉人',
        on_delete=models.CASCADE)
    reported_case = models.ForeignKey(Case,
        related_name='beReported',  #accused
        null=True, blank=True,
        verbose_name='被檢舉的委託單',
        on_delete=models.SET_NULL)
    reported_user = models.ForeignKey(UserDetail,
        related_name='beReported', #accused
        null=True, blank=True,
        verbose_name='被檢舉人',
        on_delete=models.SET_NULL)

    # 內容
    report_type = models.ForeignKey(ReportType,
        related_name='reports',
        verbose_name='檢舉類型',
        null=True, blank=True,
        on_delete=models.SET_NULL)
    description = models.TextField(
        default='', blank=True,
        verbose_name='內容描述')

    # 時間
    created_datetime = models.DateTimeField(auto_now_add=True,
        verbose_name='建立時間')

    # 狀態
    is_treated = models.BooleanField(
        default=False,
        verbose_name='是否已處理',
        help_text='0:未處理，1:已處理')
    is_valid = models.BooleanField(
        default=None,
        null=True, blank=True,
        verbose_name='檢舉是否成立',
        help_text='0:不成立（無效的檢舉），1:成立（有效的檢舉）')

    class Meta:
        verbose_name = '檢舉'  # 給人看的 table 名稱
        ordering = ['-created_datetime']

    def __str__(self):  # 拿去 print() 時要怎麼顯示
        return f'[{self.report_type}]{self.reporter}: {self.description}'
