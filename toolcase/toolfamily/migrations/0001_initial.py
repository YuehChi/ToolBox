# Generated by Django 3.1 on 2022-03-23 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import toolfamily.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('case_id', models.IntegerField(default=toolfamily.models.IntUUID, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=30, verbose_name='標題')),
                ('description', models.TextField(default='', verbose_name='內容說明')),
                ('reward', models.CharField(default='', max_length=50, verbose_name='報酬方式')),
                ('location', models.CharField(blank=True, default='', max_length=50, verbose_name='地點')),
                ('constraint', models.CharField(blank=True, default='', max_length=50, verbose_name='偏好條件')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('started_datetime', models.DateTimeField(blank=True, default=None, null=True, verbose_name='開始時間')),
                ('ended_datetime', models.DateTimeField(default=toolfamily.models.daysAfter, verbose_name='結束時間')),
                ('last_change', models.DateTimeField(auto_now=True, verbose_name='最後修改時間')),
                ('pageviews', models.IntegerField(default=0, verbose_name='瀏覽人數')),
                ('shown_public', models.BooleanField(default=True, help_text='False:不顯示在公開查詢頁面，但已應徵/接案者仍可繼續', verbose_name='是否公開顯示')),
            ],
            options={
                'verbose_name': '委託單',
                'ordering': ['-created_datetime'],
            },
        ),
        migrations.CreateModel(
            name='Case_Field',
            fields=[
                ('casefield_id', models.AutoField(primary_key=True, serialize=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toolfamily.case')),
            ],
            options={
                'verbose_name': '委託-領域 關聯表',
            },
        ),
        migrations.CreateModel(
            name='Case_Type',
            fields=[
                ('casetype_id', models.AutoField(primary_key=True, serialize=False)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toolfamily.case')),
            ],
            options={
                'verbose_name': '委託-類型 關聯表',
            },
        ),
        migrations.CreateModel(
            name='ReportType',
            fields=[
                ('report_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('report_type_name', models.CharField(default='其他', max_length=50)),
            ],
            options={
                'verbose_name': '檢舉類型',
                'ordering': ['report_type_id'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(default='其他', help_text='0:關閉，1:徵求，2:進行，3:完成', max_length=10, verbose_name='狀態名稱')),
            ],
            options={
                'verbose_name': '委託狀態',
            },
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('user_id', models.IntegerField(default=toolfamily.models.IntUUID, editable=False, primary_key=True, serialize=False)),
                ('account_mail', models.EmailField(max_length=30, unique=True, verbose_name='帳號（電子郵件）')),
                ('salt', models.TextField(default=toolfamily.models.IntUUID, verbose_name='隨機雜湊')),
                ('verification', models.BooleanField(default=False, help_text='0:未驗證，1:已驗證', verbose_name='信箱是否驗證')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('name', models.CharField(default='', max_length=10, verbose_name='真實姓名')),
                ('nickname', models.CharField(blank=True, default='', help_text='主頁上對他人是顯示這個', max_length=50, verbose_name='暱稱')),
                ('gender', models.IntegerField(default=0, help_text='0:不願透露，1:男，2:女，3往後是其他', verbose_name='生理性別')),
                ('department', models.CharField(blank=True, default='', max_length=30, verbose_name='科系')),
                ('contact', models.TextField(default='', help_text='使用者另外填寫的聯絡方式，可以是 line id、messenger 等任意內容', verbose_name='聯絡方式')),
                ('information', models.TextField(blank=True, default='', verbose_name='自我介紹')),
                ('rate', models.FloatField(default=0, verbose_name='評價')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='images/userIcon/')),
                ('isActive', models.BooleanField(default=True, help_text='如果使用者想刪帳號/被永久封號，就把帳號改成停用', verbose_name='帳號是否啟用')),
                ('django_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_detail', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '使用者',
            },
        ),
        migrations.CreateModel(
            name='UserReportedRecord',
            fields=[
                ('record_id', models.IntegerField(default=toolfamily.models.IntUUID, editable=False, primary_key=True, serialize=False)),
                ('take_expiry_date', models.DateTimeField(blank=True, default=None, help_text='若沒有被停權則為空', null=True, verbose_name='接案停權到期日')),
                ('publish_expiry_date', models.DateTimeField(blank=True, default=None, help_text='若沒有被停權則為空', null=True, verbose_name='發布停權到期日')),
                ('take_ban_times', models.SmallIntegerField(blank=True, default=0, help_text='累積達三次則永久停權', null=True, verbose_name='接案停權累積次數')),
                ('publish_ban_times', models.SmallIntegerField(blank=True, default=0, help_text='累積達三次則永久停權', null=True, verbose_name='發布停權累積次數')),
                ('reported_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='report_record', to='toolfamily.userdetail', verbose_name='使用者')),
            ],
            options={
                'verbose_name': '停權紀錄',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(default='其他', max_length=10, verbose_name='類型名稱')),
                ('case', models.ManyToManyField(through='toolfamily.Case_Type', to='toolfamily.Case')),
            ],
            options={
                'verbose_name': '委託類型',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.IntegerField(default=toolfamily.models.IntUUID, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, default='', verbose_name='內容描述')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='建立時間')),
                ('is_treated', models.BooleanField(default=False, help_text='0:未處理，1:已處理', verbose_name='是否已處理')),
                ('is_valid', models.BooleanField(blank=True, default=None, help_text='0:不成立（無效的檢舉），1:成立（有效的檢舉）', null=True, verbose_name='檢舉是否成立')),
                ('report_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='toolfamily.reporttype', verbose_name='檢舉類型')),
                ('reported_case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='beReported', to='toolfamily.case', verbose_name='被檢舉的委託單')),
                ('reported_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='beReported', to='toolfamily.userdetail', verbose_name='被檢舉人')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='toolfamily.userdetail', verbose_name='檢舉人')),
            ],
            options={
                'verbose_name': '檢舉',
                'ordering': ['-created_datetime'],
            },
        ),
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('followuser_id', models.IntegerField(default=toolfamily.models.IntUUID, editable=False, primary_key=True, serialize=False)),
                ('followed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='toolfamily.userdetail', verbose_name='追蹤的用戶')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_users', to='toolfamily.userdetail', verbose_name='跟隨者')),
            ],
            options={
                'verbose_name': '追蹤使用者',
            },
        ),
        migrations.CreateModel(
            name='FollowCase',
            fields=[
                ('followcase_id', models.IntegerField(default=toolfamily.models.IntUUID, editable=False, primary_key=True, serialize=False)),
                ('followed_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='toolfamily.case', verbose_name='追蹤的委託')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_cases', to='toolfamily.userdetail', verbose_name='跟隨者')),
            ],
            options={
                'verbose_name': '追蹤委託',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('field_id', models.AutoField(primary_key=True, serialize=False)),
                ('field_name', models.CharField(default='其他', max_length=10, verbose_name='領域名稱')),
                ('case', models.ManyToManyField(through='toolfamily.Case_Field', to='toolfamily.Case')),
            ],
            options={
                'verbose_name': '委託領域',
            },
        ),
        migrations.AddField(
            model_name='case_type',
            name='case_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toolfamily.type'),
        ),
        migrations.AddField(
            model_name='case_field',
            name='case_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='toolfamily.field'),
        ),
        migrations.AddField(
            model_name='case',
            name='case_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='case', to='toolfamily.status', verbose_name='狀態'),
        ),
        migrations.AddField(
            model_name='case',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='toolfamily.userdetail', verbose_name='委託人'),
        ),
        migrations.CreateModel(
            name='CommissionRecord',
            fields=[
                ('commissionrecord_id', models.IntegerField(default=toolfamily.models.IntUUID, editable=False, primary_key=True, serialize=False)),
                ('rate_publisher_to_worker', models.SmallIntegerField(blank=True, default=None, help_text='委託人給工具人的評價，整數 1-5', null=True, verbose_name='工具人評價')),
                ('rate_worker_to_publisher', models.SmallIntegerField(blank=True, default=None, help_text='工具人給委託人的評價，整數 1-5', null=True, verbose_name='委託人評價')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, help_text='原則上是委託人確定委託工具人的時間點', verbose_name='成案時間')),
                ('finish_datetime', models.DateTimeField(blank=True, default=None, help_text='工具人按下確定的時間點', null=True, verbose_name='完成時間')),
                ('doublecheck_datetime', models.DateTimeField(blank=True, default=None, help_text='委託人按下確定的時間點', null=True, verbose_name='雙重確認-完成時間')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commission_record', to='toolfamily.case', verbose_name='委託單')),
                ('commissioned_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commission_record', to='toolfamily.userdetail', verbose_name='接案的工具人')),
                ('user_status', models.ForeignKey(help_text='使用者_維修單狀態，若是工具人身分，則此欄位用於判斷使用者在維修單上的按鈕狀態，及該維修單在使用者個人頁面狀態', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commission_record', to='toolfamily.status', verbose_name='狀態')),
            ],
            options={
                'verbose_name': '承接紀錄',
                'order_with_respect_to': 'case',
            },
        ),
        migrations.CreateModel(
            name='CaseWillingness',
            fields=[
                ('casewillingness_id', models.IntegerField(default=toolfamily.models.IntUUID, editable=False, primary_key=True, serialize=False)),
                ('recommendation', models.TextField(blank=True, default='', verbose_name='附加資訊')),
                ('created_datetime', models.DateTimeField(auto_now_add=True, verbose_name='應徵時間')),
                ('apply_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applyed_by', to='toolfamily.case', verbose_name='委託單')),
                ('willing_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applys', to='toolfamily.userdetail', verbose_name='應徵的工具人')),
            ],
            options={
                'verbose_name': '應徵',
                'order_with_respect_to': 'apply_case',
            },
        ),
        migrations.CreateModel(
            name='CasePhoto',
            fields=[
                ('casephoto_id', models.IntegerField(default=toolfamily.models.IntUUID, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='images/casePhoto/')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='toolfamily.case', verbose_name='委託')),
            ],
            options={
                'verbose_name': '委託單照片',
                'order_with_respect_to': 'case',
            },
        ),
    ]
