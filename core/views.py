
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Avg
from decouple import config
from acceso.utils.decoradores import login_requerido
from acceso.models import Usuario
from .models import Imagen
from .models import ComentarioEvaluacion
import bcrypt
from acceso.forms import UsuarioForm
from core.forms import UsuarioFormBasico
from core.forms import UsuarioFormDetalle
from core.forms import ImageForm
from core.forms import Cambiopassword
from django.views import View
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth.decorators import user_passes_test

mapbox_access_token = config('mapbox_access_token')
google_access_token = config('google_access_token')


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
            'imagenes': imagenes,
            'googletoken': google_access_token
        }
        u1 = Usuario.objects.get(id=request.session['usuario']['id'])
        if u1.is_active is True:
            return render(request, 'core/index.html', contexto)
        else:
            return redirect(reverse('acceso:bienvenida'))

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
                messages.error(request, 'M??ximo 3 im??genes.')
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
        numeromensaje = f'https://wa.me/{numero}?text=Me%20interesa%20obtener%20mayor%20informaci??n%20de%20su%20taller'
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


class CambioPass(View):
    def get(self, request):
        form = Cambiopassword()
        contexto = {
            'formModel': form,
        }
        return render(request, 'core/cambiopass.html', contexto)

    def post(self, request):
        if request.session['usuario']:
            form = Cambiopassword(request.POST)
            if form.is_valid():
                user = Usuario.objects.filter(Q(username=request.session['usuario']['username']) | Q(
                    email=request.session['usuario']['email'])).first()
                if user:
                    form_password = form.cleaned_data['new_password']
                    if bcrypt.checkpw(form_password.encode(), user.password.encode()):
                        if request.POST['password'] == request.POST['confirmar_new_password']:
                            usuario_form = form.save(commit=False)
                            nueva_contrase??a = bcrypt.hashpw(
                                usuario_form.password.encode(), bcrypt.gensalt()).decode()
                            usuario_detail = Usuario.objects.get(
                                id=request.session['usuario']['id'])
                            usuario_detail.password = nueva_contrase??a
                            usuario_detail.save()
                            messages.success(
                                request, 'Contrase??a Actualizada con exito.')
                            return redirect(reverse('dashboard:index'))
                        else:
                            messages.error(
                                request, 'Las nuevas contrase??as no coinciden.')
                            return redirect(reverse('dashboard:cambiopass'))
                    else:
                        messages.error(
                            request, 'Contrase??a actual no v??lida.')
                        return redirect(reverse('dashboard:cambiopass'))
            else:
                messages.error(
                    request, 'Informacion ingresada Con errores, solucionar')
                return redirect(reverse('dashboard:cambiopass'))
        else:
            messages.error(request, 'Tu no estas logeado.')
            return redirect(reverse('acceso:bienvenida'))
