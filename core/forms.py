from datetime import date

from django import forms

from acceso.models import Usuario

from acceso.forms import UsuarioForm

from .models import Imagen

import re


class UsuarioFormDetalle(UsuarioForm):
    confirmar_password = None

    class Meta:
        model = Usuario
        fields = ['nombre_taller', 'direccion', 'telefono',
                  'instagram', 'facebook', 'descripcion']

        labels = {
            'nombre_taller': 'Nombre de tu Taller: ',
            'direccion': 'Dirección: ',
            'telefono': 'Número de contacto, Whatsapp: ',
            'instagram': 'Link Instagram: ',
            'facebook': 'Link Facebook: ',
            'descripcion': 'Describe tus Servicios:',
        }

        widgets = {
            'nombre_taller': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'id': 'searchTextField', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }


class UsuarioFormBasico(UsuarioForm):
    confirmar_password = None

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'username', 'email']

        labels = {
            'nombre': 'Nombre: ',
            'apellido': 'Apellido: ',
            'username': 'Nombre Usuario: ',
            'email': 'Correo: ',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
        }


class ImageForm(forms.ModelForm):

    class Meta:
        model = Imagen
        fields = ['image']

        labels = {
            'image': 'Imagen (máx 2mb):'
        }

        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control form-control-sm', 'type': 'file', 'id': 'formFileSm', 'accept': 'images/'}),
        }


class Cambiopassword(forms.ModelForm):
    confirmar_password = None
    nombre = None
    apellido = None
    username = None
    email = None

    new_password = forms.CharField(
        label="Contraseña Actual:", widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))
    confirmar_new_password = forms.CharField(
        label="Confirmar Nueva Contraseña:", widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': True}))

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        if cleaned_data.get('password') != cleaned_data.get('confirmar_new_password'):
            raise forms.ValidationError(
                "Las nuevas contraseñas no coinciden"
            )

    class Meta:
        model = Usuario

        fields = ['new_password', 'password', 'confirmar_new_password']
        labels = {
            'password': 'Nueva Contraseña: ',
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': True}),
        }
