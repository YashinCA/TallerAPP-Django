from datetime import date

from django import forms

from acceso.models import Usuario
from core.models import ComentarioEvaluacion

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(
    r'^([a-zA-Z ]{2,254})')


class UsuarioForm(forms.ModelForm):

    # agregar validaciones de email, nombre, apellido, contraseña, telefono

    confirmar_password = forms.CharField(
        label="Confirmar Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if len(nombre) < 2:
            raise forms.ValidationError(
                'Nombre debe tener minimo 2 caracteres ')
        if not NOMBRE_REGEX.match(nombre):
            raise forms.ValidationError('Nombre Solo debe contener letras')
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if len(apellido) < 2:
            raise forms.ValidationError(
                'apellido debe tener minimo 2 caracteres')
        if not NOMBRE_REGEX.match(apellido):
            raise forms.ValidationError('apellido Solo debe contener letras')
        return apellido

    def clean_email(self):
        email = self.cleaned_data['email']
        if not EMAIL_REGEX.match(email):
            raise forms.ValidationError(
                'Ingresar formato válido de Correo Electronico')
        return email

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        if cleaned_data.get('password') != cleaned_data.get('confirmar_password'):
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
            )

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'username', 'email', 'password']

        labels = {
            'nombre': 'Nombre: ',
            'apellido': 'Apellido: ',
            'username': 'Nombre Usuario: ',
            'email': 'Correo: ',
            'password': 'Contraseña: ',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioEvaluacion
        fields = ['evaluacion', 'nombre', 'comentario']

        labels = {
            'evaluacion': 'Evaluación: ',
            'nombre': 'Nombre: ',
            'comentario': 'Comentario: ',
        }

        widgets = {
            'evaluacion': forms.TextInput(attrs={'class': 'rating', 'id': 'input-id', 'value': '0', 'type': 'text', 'data-min': '0', 'data-max': '5', 'data-step': '0.5', 'data-size': 'xs', 'name': 'evaluacion', 'tabindex': '-1', 'required': True}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
        }


class change_password_Form(forms.ModelForm):

    # agregar validaciones de email, nombre, apellido, contraseña, telefono

    confirmar_password = forms.CharField(
        label="Confirmar nueva contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        if cleaned_data.get('password') != cleaned_data.get('confirmar_password'):
            raise forms.ValidationError(
                "Las contraseñas no coinciden"
            )

    class Meta:
        model = Usuario
        fields = ['password']

        labels = {
            'password': 'Nueva contraseña: ',
        }

        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


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


class ForgetPass(LoginForm):
    password = None

    username = forms.CharField(
        label='Usuario o Email:',
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )
