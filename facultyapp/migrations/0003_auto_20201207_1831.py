# Generated by Django 3.0.6 on 2020-12-07 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facultyapp', '0002_auto_20201128_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='cnt',
            field=models.CharField(max_length=12),
        ),
    ]
