# Generated by Django 5.0.3 on 2024-07-10 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0004_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='authenticated',
            field=models.BooleanField(blank=True, null=True, verbose_name='احراز هویت شده'),
        ),
    ]
