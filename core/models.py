from django.db import models
from acceso.models import Usuario
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


# class Usuario(models.Model):
#     nombre = models.CharField(max_length=50)
#     apellido = models.CharField(max_length=50)
#     username = models.CharField(
#         max_length=20, unique=True, verbose_name="Nombre de Usuario")
#     telefono = models.CharField(
#         max_length=12, unique=True, null=True, blank=True)
#     email = models.EmailField(max_length=200, unique=True)
#     propietario_taller = models.BooleanField(default=True)
#     # para efectos de la actividad, será por defecto true
#     nombre_taller = models.CharField(max_length=200, null=True, blank=True)
#     instagram = models.charField(
#         max_length=100, unique=True, null=True, blank=True)
#     facebook = models.charField(
#         max_length=100, unique=True, null=True, blank=True)
#     direccion = models.TextField(null=True, blank=True)
#     lat = models.FloatField(blank=True, null=True)
#     long = models.FloatField(blank=True, null=True)
#     password = models.CharField(max_length=72)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# images: lista de imagenes asociadas a un taller
# comentarios: lista de comentarios asociados a un taller

class Imagen(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    usuario = models.ForeignKey(
        Usuario, related_name="images", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ComentarioEvaluacion(models.Model):
    usuario = models.ForeignKey(
        Usuario, related_name="comentarios", on_delete=models.CASCADE)
    # Despues de comprobar si todo funciona correctamente, cambiar a False
    nombre = models.CharField(max_length=50, blank=True, null=True)
    comentario = models.TextField(max_length=350, blank=True, null=True)
    evaluacion = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    # evaluacion = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
