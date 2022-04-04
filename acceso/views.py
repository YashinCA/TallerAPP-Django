from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.db.models import Avg
from django.urls import reverse
from django.views import View
from django.contrib import messages
from acceso.forms import UsuarioForm, change_password_Form, forgetPasswordForm
from acceso.forms import ComentarioForm
from acceso.models import Usuario
from core.models import ComentarioEvaluacion
from core.models import Imagen
import bcrypt
# email stuff
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


mapbox_access_token = 'pk.eyJ1IjoieWNhcnJpbGxvIiwiYSI6ImNsMHVjbTBxZTA0bzYza28ydGp4eDNreHgifQ.KDy-xFRWYKKA7pPaBofapg'


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Usuario o Email'})
    )

    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )


def welcome(request):
    contexto = {
        'formLogin': LoginForm()
    }
    if 'usuario' in request.session:
        del request.session['usuario']
    return render(request, 'acceso/bienvenida.html', contexto)


class LoginView(View):

    def get(self, request):

        if 'usuario' in request.session and request.session['usuario']['is_active'] == True:
            messages.error(
                request, 'Ya estas logueado. Si quieres salir, click en SALIR')
            # return redirect('/')
            return redirect(reverse('dashboard:index'))

        contexto = {
            'formRegister': UsuarioForm(),
            'formLogin': LoginForm()
        }

        return render(request, 'acceso/login.html', contexto)

    def post(self, request):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = bcrypt.hashpw(
                usuario.password.encode(), bcrypt.gensalt()).decode()
            #inactive_user = send_verification_email(request, form)
            # inactive_user.cleaned_data['email']
            usuario.is_active = False
            usuario.save()
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta de Taller APP'
            message = render_to_string('acc_active_email.html', {
                'user': usuario,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
                'token': account_activation_token.make_token(usuario),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            # user = Usuario.objects.filter(Q(username=form.cleaned_data['username']) | Q(
            #     email=form.cleaned_data['username'])).first()
            # messages.success(request, 'Usuario creado correctamente')
            # request.session['usuario'] = {
            #     'nombre': user.nombre, 'apellido': user.apellido, 'email': user.email, 'username': user.username, 'id': user.id}
            # return redirect('/')
            return HttpResponse('Por favor confirma tu correo para completar el registro')
        else:

            contexto = {
                'formRegister': form,
                'formLogin': LoginForm()
            }

            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'acceso/login.html', contexto)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = Usuario.objects.filter(Q(username=form.cleaned_data['username']) | Q(
                email=form.cleaned_data['username'])).first()
            if user:
                if user.is_active == True:
                    form_password = form.cleaned_data['password']
                    if bcrypt.checkpw(form_password.encode(), user.password.encode()):
                        request.session['usuario'] = {
                            'nombre': user.nombre, 'apellido': user.apellido, 'email': user.email, 'username': user.username, 'id': user.id, 'password': user.password}
                        # return redirect('/')
                        return redirect(reverse('dashboard:index'))
                    else:
                        messages.error(
                            request, 'Contraseña o Usuario Incorrecto')
                        return redirect(reverse('acceso:bienvenida'))
                else:
                    messages.error(
                        request, 'No has activado tu cuenta, debes hacerlo desde el correo con el que te registraste.')
                    return redirect(reverse('acceso:bienvenida'))
            else:
                messages.error(
                    request, 'Usuario No Existe, Registrate.')
                return redirect(reverse('acceso:bienvenida'))
        else:
            contexto = {
                'formRegister': UsuarioForm(),
                'formLogin': form
            }
            return render(request, 'acceso/login.html', contexto)


def logout(request):

    if 'usuario' in request.session:
        messages.success(request, 'SALISTE')
        del request.session['usuario']
    else:
        messages.error(request, 'Tu no estas logeado.')

    # return redirect(reverse('acceso:acceso'))
    return redirect(reverse('acceso:bienvenida'))


class Talleres(View):
    def get(self, request):
        print('buscando error 1')
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
        return render(request, 'acceso/talleres.html', contexto)


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
            'formComent': ComentarioForm(),
            'promedio': promedio_evaluaciones,

        }
        return render(request, 'acceso/perfil.html', contexto)

    def post(self, request, pk):
        usuario_detail = Usuario.objects.get(
            id=pk)
        formComent = ComentarioForm(request.POST)
        if formComent.is_valid():
            comentario_recibido = formComent.save(commit=False)
            comentario_recibido.usuario = usuario_detail
            comentario_recibido.save()
            messages.success(request, 'Gracias por tu evaluación!')
            return redirect(f'/view/{pk}')
        else:
            messages.error(request, 'Con errores, solucionar.')
            # return render(request, 'acceso/perfil.html', {'formComent': formComent})
            return redirect(f'/view/{pk}')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request)
        # return redirect('home')
        messages.success(request, 'Usuario creado correctamente')
        return render(request, 'acceso/confirmacion.html')
    else:
        return HttpResponse('Activation link is invalid!')

def forgetpassword(request):
    if request.method == 'GET':
        contexto = {
            'forgotPasswordForm': forgetPasswordForm()
        }
        return render(request, 'acceso/forget_password.html', contexto)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        usuario = Usuario.objects.filter(username=username).first()
        if usuario is None:
            messages.error(request, 'Usuario no encontrado')
            return redirect(reverse('acceso:bienvenida'))
        else:
            current_site = get_current_site(request)
            mail_subject = 'Restore your password'
            message = render_to_string('restore_password.html', {
                'user': usuario,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
                'token': account_activation_token.make_token(usuario),
            })
            to_email = usuario.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Correo electrónico enviado')
            return HttpResponse('Por favor revisa tu correo para recuperar contraseña')

def restore_password(request, uidb64, token):
    if request.method == 'GET':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            contexto = {
                'change_password_Form': change_password_Form(),
                'usuario' : user,
            }
        return render(request, 'acceso/restablecer_password.html', contexto)
    
    if request.method == 'POST':
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
        user.password = request.POST.get('password')
        user.password = bcrypt.hashpw(
                user.password.encode(), bcrypt.gensalt()).decode()
        user.save()
        messages.success(request, 'Clave actualizada con éxtito')
        return redirect(reverse('acceso:bienvenida'))

