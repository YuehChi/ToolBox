# Generated by Django 3.1 on 2022-04-04 16:48

from django.db import migrations, models
import toolfamily.models


class Migration(migrations.Migration):

    dependencies = [
        ('toolfamily', '0003_auto_20220404_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to=toolfamily.models.user_icon_path),
        ),
    ]
