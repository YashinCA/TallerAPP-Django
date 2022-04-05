from django.contrib import admin
from .models import Usuario
from core.models import ComentarioEvaluacion
# Register your models here.

admin.site.register(Usuario)
admin.site.register(ComentarioEvaluacion)