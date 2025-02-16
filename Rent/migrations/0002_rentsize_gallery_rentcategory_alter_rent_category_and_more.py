# Generated by Django 5.0.3 on 2024-07-09 07:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rent', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RentSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(db_index=True, max_length=300, verbose_name='سایز')),
            ],
            options={
                'verbose_name': 'سایز',
                'verbose_name_plural': 'سایزها',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='images/products', verbose_name='تصاویر')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال/غیرفعال')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Rent.rent', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'گالری',
                'verbose_name_plural': 'گالری ها',
            },
        ),
        migrations.CreateModel(
            name='RentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان در url')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال/غیرفعال')),
                ('is_deleted', models.BooleanField(verbose_name='حذفشده/نشده')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Rent.rentcategory', verbose_name='دسته بندی والد')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.AlterField(
            model_name='rent',
            name='category',
            field=models.ManyToManyField(to='Rent.rentcategory', verbose_name='دسته بندی ها'),
        ),
        migrations.CreateModel(
            name='RentComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_send', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')),
                ('text', models.TextField(verbose_name='متن نظر')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Rent.rentcomment', verbose_name='والد')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rent.rent', verbose_name='مقاله')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
            },
        ),
        migrations.AlterField(
            model_name='rent',
            name='size',
            field=models.ManyToManyField(to='Rent.rentsize', verbose_name='سایز'),
        ),
        migrations.CreateModel(
            name='RentVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=30, verbose_name='آیپی کاربر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rent.rent', verbose_name='محصول')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='آیدی کاربر')),
            ],
            options={
                'verbose_name': 'بازدید',
                'verbose_name_plural': 'بازدیدها',
            },
        ),
    ]
