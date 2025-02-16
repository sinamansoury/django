# Generated by Django 5.0.3 on 2024-07-09 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0003_productcomment_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/Products', verbose_name='تصویر محصولات')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('color', models.CharField(max_length=20, null=True, verbose_name='رنگ')),
                ('count', models.IntegerField(default=1, verbose_name='تعداد')),
                ('short_description', models.CharField(db_index=True, max_length=300, null=True, verbose_name='توضیحات کوتاه')),
                ('description', models.TextField(max_length=300, verbose_name='توضیحات اصلی')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال/غیرفعال')),
                ('is_deleted', models.BooleanField(verbose_name='حذفشده/نشده')),
                ('slug', models.SlugField(default='', verbose_name='عنوان درurl')),
                ('category', models.ManyToManyField(to='product.productcategory', verbose_name='دسته بندی ها')),
                ('size', models.ManyToManyField(to='product.size', verbose_name='سایز')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
    ]
