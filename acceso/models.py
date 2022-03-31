import geocoder
from django.db import models

mapbox_access_token = 'pk.eyJ1IjoieWNhcnJpbGxvIiwiYSI6ImNsMHVjbTBxZTA0bzYza28ydGp4eDNreHgifQ.KDy-xFRWYKKA7pPaBofapg'


class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    username = models.CharField(
        max_length=20, unique=True, verbose_name="Nombre de Usuario")
    telefono = models.CharField(
        max_length=12, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    propietario_taller = models.BooleanField(default=True)
    # para efectos de la actividad, será por defecto true
    nombre_taller = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    facebook = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    descripcion = models.TextField(max_length=300, blank=True, null=True)
    direccion = models.TextField(null=True, blank=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    password = models.CharField(max_length=72)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # imagenes: lista de imagenes asociadas a un taller

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.direccion, key=mapbox_access_token)
        g = g.latlng  # [lat, long]
        self.lat = g[0]
        self.long = g[1]
        return super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"