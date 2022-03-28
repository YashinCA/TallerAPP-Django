from django import forms
from django.shortcuts import redirect, render
from django.db.models import Q
from django.urls import reverse
from django.views import View
from django.contrib import messages
from acceso.forms import UsuarioForm
from acceso.models import Usuario
from core.models import Imagen
import bcrypt
# Create your views here.

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
    return render(request, 'acceso/bienvenida.html', contexto)


class LoginView(View):

    def get(self, request):

        if 'usuario' in request.session:
            messages.error(
                request, 'YA ESTAS LOGEADO. Si quieres salir, CLICK EN SALIR!!')
            # return redirect('/')
            return redirect(reverse('dashboard:index'))

        contexto = {
            'formRegister': UsuarioForm(),
            'formLogin': LoginForm()
        }

        return render(request, 'acceso/login.html', contexto)

    def post(self, request):
        print(request.POST)

        form = UsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = bcrypt.hashpw(
                usuario.password.encode(), bcrypt.gensalt()).decode()
            usuario.save()
            user = Usuario.objects.filter(Q(username=form.cleaned_data['username']) | Q(
                email=form.cleaned_data['username'])).first()
            messages.success(request, 'Usuario creado correctamente')
            request.session['usuario'] = {
                'nombre': user.nombre, 'apellido': user.apellido, 'email': user.email, 'username': user.username, 'id': user.id}
            # return redirect('/')
            return redirect(reverse('dashboard:index'))
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
                form_password = form.cleaned_data['password']
                if bcrypt.checkpw(form_password.encode(), user.password.encode()):

                    request.session['usuario'] = {
                        'nombre': user.nombre, 'apellido': user.apellido, 'email': user.email, 'username': user.username, 'id': user.id}
                    # return redirect('/')
                    return redirect(reverse('dashboard:index'))
                else:
                    messages.error(
                        request, '1Contraseña o Email o Nombre de Usuario INCORRECTO')
            else:
                messages.error(
                    request, '2Contraseña o Email o Nombre de Usuario INCORRECTO')

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
        talleres_total = Usuario.objects.all()
        # for taller in talleres_total:
        #     print(taller.lat)
        #     print(taller.long)
        contexto = {
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
        # print(usuario_detail.long)
        # print(type(usuario_detail.lat))
        contexto = {
            'taller': usuario_detail,
            'imagenes': imagenes,
            'whatsapp': numeromensaje,
            'mapboxtoken': mapbox_access_token,
            'lat': str(usuario_detail.lat),
            'long': str(usuario_detail.long)
        }
        return render(request, 'acceso/perfil.html', contexto)
