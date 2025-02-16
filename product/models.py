import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from Account.models import User


# Create your models here.


class ProductCategory(models.Model):
    parent = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")
    url_title = models.CharField(max_length=300, db_index=True,verbose_name="عنوان در url")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")
    is_deleted = models.BooleanField(verbose_name="حذفشده/نشده")

    def __str__(self):
        return f'({self.title} , {self.url_title})'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrands(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name="نام برند")
    url_title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان در url", unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال بودن/نبودن")
    is_deleted = models.BooleanField(verbose_name="حذف شده/نشده")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'


class Size(models.Model):
    size = models.CharField(max_length=300, db_index=True, verbose_name="سایز")

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایزها'


class Product(models.Model):
    title = models.CharField(max_length=300,verbose_name='عنوان')
    image = models.ImageField(upload_to='images/Products', verbose_name="تصویر محصولات", blank=True, null=True)
    category = models.ManyToManyField(ProductCategory, verbose_name="دسته بندی ها")
    brand = models.ForeignKey(ProductBrands, verbose_name="برند", on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(null=False, verbose_name="قیمت")
    color = models.CharField(max_length=20, null=True, verbose_name="رنگ")
    size = models.ManyToManyField(Size, verbose_name="سایز")
    count = models.IntegerField(null=False, verbose_name="تعداد", default=1)
    short_description = models.CharField(max_length=300,
                                         null=True,
                                         verbose_name="توضیحات کوتاه",
                                         db_index=True)
    description = models.TextField(max_length=300,
                                   null=False,
                                   verbose_name="توضیحات اصلی")
    is_active = models.BooleanField(default=True,verbose_name='فعال/غیرفعال')
    is_deleted = models.BooleanField(verbose_name="حذفشده/نشده")
    slug = models.SlugField(default='',
                            null=False,
                            db_index=True,
                            verbose_name='عنوان درurl')

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    captions = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")
    product = models.ForeignKey(Product, verbose_name='مصحولات', on_delete=models.CASCADE, related_name='product_tags')

    def __str__(self):
        return self.captions

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ محصولات'


class ProductVisit(models.Model):
    ip_address = models.CharField(max_length=30, verbose_name="آیپی کاربر")
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name='آیدی کاربر', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.product}/{self.ip_address}'

    class Meta:
        verbose_name = 'بازدید'
        verbose_name_plural = 'بازدیدها'


class Gallery(models.Model):
    image = models.ImageField(upload_to='images/products', verbose_name="تصاویر", null=True)
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'گالری'
        verbose_name_plural = 'گالری ها'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ProductComment', on_delete=models.CASCADE, verbose_name='والد', null=True)
    date_send = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ارسال')
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='متن نظر')

    def __str__(self):
        return str(self.text)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
