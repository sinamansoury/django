from django.db import models

# Create your models here.


class ContactUs(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    email = models.EmailField(max_length=254, verbose_name='ایمیل')
    fullname = models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)
    message = models.TextField(verbose_name='متن تماس با ما')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده')
    response = models.TextField(verbose_name='پاسخ ادمین', null=True, blank=True)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.title


class ProfileImages(models.Model):
    image = models.ImageField(upload_to='uploads')
