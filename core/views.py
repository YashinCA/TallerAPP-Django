
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Avg
from acceso.utils.decoradores import login_requerido
from acceso.models import Usuario
from .models import Imagen
from .models import ComentarioEvaluacion
from acceso.forms import UsuarioForm
from core.forms import UsuarioFormBasico
from core.forms import UsuarioFormDetalle
from core.forms import ImageForm
from django.views import View
from django.contrib import messages
from django.db.models import Q, Count

mapbox_access_token = 'pk.eyJ1IjoieWNhcnJpbGxvIiwiYSI6ImNsMHVjbTBxZTA0bzYza28ydGp4eDNreHgifQ.KDy-xFRWYKKA7pPaBofapg'


class IndexView(View):
    def get(self, request):
        usuario_detail = Usuario.objects.get(
            id=request.session['usuario']['id'])
        form = UsuarioFormBasico(instance=usuario_detail)
        form_det = UsuarioFormDetalle(instance=usuario_detail)
        form_img = ImageForm(instance=usuario_detail)
        imagenes = Imagen.objects.all().filter(
            usuario__id=request.session['usuario']['id'])
        contexto = {
            'usuariodetalles': usuario_detail,
            'formModel': form,
            'formModelDet': form_det,
            'formModelImg': form_img,
            'formImg': form_img,
            'imagenes': imagenes
        }
        return render(request, 'core/index.html', contexto)

    def post(self, request):
        usuario_detail = Usuario.objects.get(
            id=request.session['usuario']['id'])
        form = UsuarioFormBasico(request.POST, instance=usuario_detail)
        form_det = UsuarioFormDetalle(request.POST, instance=usuario_detail)
        form_img = ImageForm(request.POST, request.FILES)
        image = request.FILES.get('image')
        imagenes = Imagen.objects.all().filter(
            usuario__id=request.session['usuario']['id'])
        if len(request.FILES) > 0:
            if imagenes.count() < 3:
                if form_img.is_valid() and request.FILES.get('image') != None:
                    Imagen.objects.create(image=image, usuario=usuario_detail)
                    messages.success(request, 'Imagen Cargada Correctamente.')
                    return redirect(reverse('dashboard:index'))
                else:
                    messages.error(request, 'No se ha cargado ninguna imagen.')
                    return redirect(reverse('dashboard:index'))
            else:
                messages.error(request, 'Máximo 3 imágenes.')
                return redirect(reverse('dashboard:index'))
        elif request.POST.get('form') == 'basico':
            if form.is_valid():
                form.save()
                messages.success(request, 'Datos Editados Correctamente.')
                return redirect(reverse('dashboard:index'))
            else:
                messages.error(request, 'Con errores, solucionar.')
                return redirect(reverse('dashboard:index'))
        elif request.POST.get('form') == 'datos':
            if form_det.is_valid():
                form_det.save()
                messages.success(
                    request, 'Datos de Taller Actualizados Correctamente.')
                return redirect(reverse('dashboard:index'))
            else:
                messages.error(request, 'Con errores, solucionar.')
                return redirect(reverse('dashboard:index'))
        else:
            messages.error(request, 'Este formulario no existe.')
            return redirect(reverse('dashboard:index'))


class DeleteImage(View):
    def get(self, request, pk):
        imagen_delete = Imagen.objects.get(id=pk)
        if request.session['usuario']['id'] == imagen_delete.usuario.id:
            imagen_delete.delete()
            messages.success(request, 'Imagen eliminada correctamente.')
            return redirect(reverse('dashboard:index'))
        else:
            messages.error(
                request, 'Esta imagen no fue subida por ti, no puedes editar.')
            return redirect(reverse('dashboard:index'))


class Detail(View):
    def get(self, request, pk):
        usuario_detail = Usuario.objects.get(
            id=pk)
        numero = str(usuario_detail.telefono)
        numero = numero[1:]
        numeromensaje = f'https://wa.me/{numero}?text=Me%20interesa%20obtener%20mayor%20información%20de%20su%20taller'
        imagenes = Imagen.objects.all().filter(
            usuario__id=pk)
        comentarios = ComentarioEvaluacion.objects.all().filter(usuario__id=pk)
        promedio_evaluaciones = ComentarioEvaluacion.objects.all().filter(
            usuario__id=pk).aggregate(Avg('evaluacion'))
        contexto = {
            'taller': usuario_detail,
            'imagenes': imagenes,
            'comentarios': comentarios,
            'whatsapp': numeromensaje,
            'mapboxtoken': mapbox_access_token,
            'lat': str(usuario_detail.lat),
            'long': str(usuario_detail.long),
            'promedio': promedio_evaluaciones,
        }
        return render(request, 'core/perfil.html', contexto)


class Talleres(View):
    def get(self, request):
        talleres_total = Usuario.objects.all()
        lista_evaluaciones = []
        for taller in talleres_total:
            identificacion = taller.id
            evaluacion_promedio = ComentarioEvaluacion.objects.all().filter(
                usuario__id=taller.id).aggregate(Avg('evaluacion'))
            if evaluacion_promedio['evaluacion__avg'] != None:
                lista_evaluaciones.append(
                    [identificacion, evaluacion_promedio['evaluacion__avg']])
        contexto = {
            'evaluaciones': lista_evaluaciones,
            'talleres': talleres_total,
            'mapboxtoken': mapbox_access_token,
        }
        return render(request, 'core/talleres.html', contexto)
