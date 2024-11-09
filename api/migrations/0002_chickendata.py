# Generated by Django 5.1.3 on 2024-11-08 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChickenData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jumlah_ayam', models.IntegerField(default=0)),
                ('mortalitas', models.FloatField(default=0.0)),
                ('usia_ayam', models.IntegerField(default=0)),
            ],
        ),
    ]