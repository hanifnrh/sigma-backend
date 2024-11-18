# Generated by Django 5.1.3 on 2024-11-18 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_parameter_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
