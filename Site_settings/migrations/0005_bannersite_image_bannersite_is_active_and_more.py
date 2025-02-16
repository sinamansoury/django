# Generated by Django 5.0.3 on 2024-06-20 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site_settings', '0004_bannersite'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannersite',
            name='image',
            field=models.ImageField(default='hell', upload_to='images/banner', verbose_name='تصویر'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bannersite',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال/غیرفعال'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bannersite',
            name='position',
            field=models.CharField(choices=[('product-list', 'صفحه محصولات'), ('product-detail', 'صفحه جزئیات محصولات')], default='product-list', max_length=100, verbose_name='موقعیت'),
            preserve_default=False,
        ),
    ]
