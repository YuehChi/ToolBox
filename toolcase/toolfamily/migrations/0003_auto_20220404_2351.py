# Generated by Django 3.1 on 2022-04-04 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolfamily', '0002_auto_20220404_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='images/userIcon/filename'),
        ),
    ]