# Generated by Django 4.0.3 on 2022-03-30 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolfamily', '0002_alter_userdetail_last_login_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='last_login_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='上次登入時間'),
        ),
    ]
