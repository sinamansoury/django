# Generated by Django 5.0.3 on 2024-07-16 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0007_authuser_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='کدملی'),
        ),
        migrations.AlterField(
            model_name='authuser',
            name='address_auth',
            field=models.IntegerField(verbose_name=' کد پستی:'),
        ),
        migrations.AlterField(
            model_name='authuser',
            name='address_auth_pic',
            field=models.ImageField(upload_to='images/auth', verbose_name='عکس تاییدیه پستی:'),
        ),
        migrations.AlterField(
            model_name='authuser',
            name='back_pic',
            field=models.ImageField(upload_to='images/auth', verbose_name='عکس پشت کارت ملی:'),
        ),
        migrations.AlterField(
            model_name='authuser',
            name='front_pic',
            field=models.ImageField(upload_to='images/auth', verbose_name='عکس روی کارت ملی:'),
        ),
        migrations.AlterField(
            model_name='authuser',
            name='pic',
            field=models.ImageField(upload_to='images/auth', verbose_name='عکس کاربر :'),
        ),
    ]
