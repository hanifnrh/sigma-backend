# Generated by Django 5.1.3 on 2024-11-12 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_startfarming'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataayam',
            name='tanggal_mulai',
            field=models.DateField(default=datetime.date(2024, 11, 12)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataayamhistory',
            name='tanggal_mulai',
            field=models.DateField(default=datetime.date(2024, 11, 12)),
            preserve_default=False,
        ),
    ]
