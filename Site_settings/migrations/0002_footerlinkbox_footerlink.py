# Generated by Django 5.0.3 on 2024-05-16 15:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterLinkBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': ' دسته بندی لینک فوتر',
                'verbose_name_plural': ' دسته بندی لینک های فوتر',
            },
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('links', models.URLField(verbose_name='لینک')),
                ('footer_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Site_settings.footerlinkbox', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'لینک  فوتر ',
                'verbose_name_plural': 'لینک های فوتر',
            },
        ),
    ]
