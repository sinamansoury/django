# Generated by Django 5.0.3 on 2024-07-09 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Site_settings', '0009_sitesettings_instagram_sitesettings_telegram'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footerlink',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='footerlink',
            name='telegram',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='telegram',
        ),
    ]
