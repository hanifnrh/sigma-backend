# Generated by Django 5.1.3 on 2024-11-08 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ammonia', models.FloatField()),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
            ],
        ),
    ]