# Generated by Django 5.1.3 on 2024-11-15 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_dataayam_tanggal_mulai_dataayamhistory_tanggal_mulai'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='score',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
