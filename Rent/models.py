from django.db import models
from django.urls import reverse

from Account.models import User
from product.models import ProductCategory, Size


# Create your models here.
class RentCategory(models.Model):
    parent = models.ForeignKey('RentCategory', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")
    url_title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان در url")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")
    is_deleted = models.BooleanField(verbose_name="حذفشده/نشده")

    def __str__(self):
        return f'({self.title} , {self.url_title})'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class RentSize(models.Model):
    size = models.CharField(max_length=300, db_index=True, verbose_name="سایز")

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایزها'


class RentDay(models.Model):
    text = models.TextField(verbose_name='بازه')

    def __str__(self):
        return str(self.text)

    class Meta:
        verbose_name = 'بازه'
        verbose_name_plural = 'بازه ها'


class Rent(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/Products', verbose_name="تصویر محصولات", blank=True, null=True)
    category = models.ManyToManyField(RentCategory, verbose_name="دسته بندی ها")
    price = models.IntegerField(null=False, verbose_name="قیمت")
    color = models.CharField(max_length=20, null=True, verbose_name="رنگ")
    size = models.ManyToManyField(RentSize, verbose_name="سایز")
    day = models.ManyToManyField(RentDay, verbose_name="بازه")
    count = models.IntegerField(null=False, verbose_name="تعداد", default=1)
    short_description = models.CharField(max_length=300,
                                         null=True,
                                         verbose_name="توضیحات کوتاه",
                                         db_index=True)
    description = models.TextField(max_length=300,
                                   null=False,
                                   verbose_name="توضیحات اصلی")
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    is_deleted = models.BooleanField(verbose_name="حذفشده/نشده")
    slug = models.SlugField(default='',
                            null=False,
                            db_index=True,
                            verbose_name='عنوان درurl')

    def get_absolute_url(self):
        return reverse('rent_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class RentVisit(models.Model):
    ip_address = models.CharField(max_length=30, verbose_name="آیپی کاربر")
    product = models.ForeignKey(Rent, verbose_name='محصول', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name='آیدی کاربر', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.product}/{self.ip_address}'

    class Meta:
        verbose_name = 'بازدید'
        verbose_name_plural = 'بازدیدها'


class Gallery(models.Model):
    image = models.ImageField(upload_to='images/products', verbose_name="تصاویر", null=True)
    product = models.ForeignKey(Rent, verbose_name='محصول', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'گالری'
        verbose_name_plural = 'گالری ها'


class RentComment(models.Model):
    product = models.ForeignKey(Rent, on_delete=models.CASCADE, verbose_name='محصول')
    parent = models.ForeignKey('RentComment', on_delete=models.CASCADE, verbose_name='والد', null=True)
    date_send = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ارسال')
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='متن نظر')

    def __str__(self):
        return str(self.text)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'



