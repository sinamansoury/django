# Generated by Django 5.0.3 on 2024-07-08 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site_settings', '0005_bannersite_image_bannersite_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='footerlink',
            name='value',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='مقدار'),
        ),
    ]
