from django.db import models

# Create your models here.


class SiteSettings(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام سایت')
    domain = models.CharField(max_length=100, verbose_name='دامنه سایت')
    phone_number = models.CharField(max_length=20, verbose_name='تلفن', null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', null=True, blank=True)
    address = models.TextField(verbose_name='ادرس')
    about_us = models.TextField(verbose_name='توضیح')
    copyright = models.TextField(verbose_name='حق کپی رایت')
    logo = models.ImageField(upload_to='images/logo/', verbose_name='لوگو')
    is_main_settings = models.BooleanField(default=True, verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.name


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')

    class Meta:
        verbose_name = ' دسته بندی لینک فوتر'
        verbose_name_plural = ' دسته بندی لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    links = models.URLField(verbose_name='لینک', null=True, blank=True)
    footer_link = models.ForeignKey(FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی')
    value = models.CharField(max_length=50, null=True, blank=True, verbose_name='مقدار')

    class Meta:
        verbose_name = 'لینک  فوتر '
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return self.title


class BannerSite(models.Model):
    class BannerSitePosition(models.TextChoices):
        product_list = 'product-list', 'صفحه محصولات'
        product_detail = 'product-detail', 'صفحه جزئیات محصولات'

    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.URLField(max_length=200, null=True, blank=True, verbose_name='عنوان در url')
    image = models.ImageField(upload_to='images/banner', verbose_name='تصویر')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')
    position = models.CharField(max_length=100, choices=BannerSitePosition.choices, verbose_name='موقعیت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر سایت'
        verbose_name_plural = 'بنرهای سایت'
