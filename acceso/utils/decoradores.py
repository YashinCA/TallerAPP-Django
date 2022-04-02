
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def login_requerido(function):
    def wrap(request, *args, **kwargs):

        if 'usuario' not in request.session:
            # if request.session['usuario']['is_active'] == False:
            #     messages.error(request, 'No has activado tu correo')
            messages.error(request, 'No estás logeado')
            return redirect(reverse('acceso:bienvenida'))

        return function(request, *args, **kwargs)

    return wrap
