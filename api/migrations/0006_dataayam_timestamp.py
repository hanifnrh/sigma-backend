# Generated by Django 5.1.3 on 2024-11-09 12:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_delete_chickenfarm'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataayam',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
