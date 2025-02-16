# Generated by Django 5.0.3 on 2024-07-10 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0005_user_authenticated'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_auth_pic', models.ImageField(upload_to='images/auth', verbose_name='عکس تاییدیه پستی')),
                ('address_auth', models.IntegerField(verbose_name='تاییدیه کد پستی')),
                ('front_pic', models.ImageField(upload_to='images/auth', verbose_name='عکس جلو')),
                ('back_pic', models.ImageField(upload_to='images/auth', verbose_name='عکس پشت')),
                ('pic', models.ImageField(upload_to='images/auth', verbose_name='عکس کاربر با کارت ملی')),
            ],
            options={
                'verbose_name': 'احراز',
                'verbose_name_plural': 'احرازها',
            },
        ),
    ]
