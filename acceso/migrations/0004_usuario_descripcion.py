# Generated by Django 4.0.2 on 2022-03-22 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceso', '0003_usuario_delete_usuariotaller'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='descripcion',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
