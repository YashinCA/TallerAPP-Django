from django.contrib import admin
from .models import Usuario
from core.models import ComentarioEvaluacion, Imagen
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Imagen)
admin.site.register(ComentarioEvaluacion)
