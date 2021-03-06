# Generated by Django 4.0.2 on 2022-03-30 02:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acceso', '0004_usuario_descripcion'),
        ('core', '0003_alter_imagen_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComentarioEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('comentario', models.TextField(blank=True, max_length=350, null=True)),
                ('evaluacion', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='acceso.usuario')),
            ],
        ),
    ]
