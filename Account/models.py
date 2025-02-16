from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='نام خانوادگی')
    avatar = models.ImageField(upload_to='images/profile', verbose_name='تصویر اواتار', null=True, blank=True)
    email_verified = models.CharField(max_length=100, unique=True, verbose_name='فعالسازی ایمیل', null=True, blank=True)
    id_code = models.IntegerField(verbose_name='کدملی', null=True, blank=True)
    birthday = models.CharField(max_length=10, verbose_name='تاریخ تولد', null=True, blank=True)
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    phone = models.IntegerField(null=True, blank=True, verbose_name='شماره موبایل')
    authenticated = models.BooleanField(null=True, blank=True, verbose_name='احراز هویت شده')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()

        return self.username


class AuthUser(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نام کاربر', null=True, blank=True)
    address_auth_pic = models.ImageField(upload_to='images/auth', verbose_name='عکس تاییدیه پستی:')
    address_auth = models.IntegerField(verbose_name=' کد پستی:')
    front_pic = models.ImageField(upload_to='images/auth', verbose_name='عکس روی کارت ملی:')
    back_pic = models.ImageField(upload_to='images/auth', verbose_name='عکس پشت کارت ملی:')
    pic = models.ImageField(upload_to='images/auth', verbose_name='عکس کاربر :')

    class Meta:
        verbose_name = 'احراز'
        verbose_name_plural = 'احرازها'

    def __str__(self):
        return str(self.user_name) if self.user_name else 'No User'
