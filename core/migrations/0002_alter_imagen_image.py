# Generated by Django 4.0.2 on 2022-03-23 01:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(['jpg'])]),
        ),
    ]
