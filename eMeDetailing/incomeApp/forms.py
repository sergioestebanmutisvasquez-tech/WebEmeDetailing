import re
from datetime import datetime, timedelta, date, time
from PIL import Image
from django import forms
from django.contrib.auth.models import User
from .models import Ingreso


class FormIngreso(forms.ModelForm):

    class Meta:
        model = Ingreso
        exclude = ['cliente', 'servicio_fk', 'estado']

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']

        if not telefono.isdigit():
            raise forms.ValidationError(
                "El teléfono debe contener solo números."
            )

        if len(telefono) != 9:
            raise forms.ValidationError(
                "El teléfono debe tener exactamente 9 números."
            )

        return telefono

    def clean_fechaReserva(self):
        fecha = self.cleaned_data['fechaReserva']
        if fecha < date.today():
            raise forms.ValidationError("La fecha no puede ser anterior a hoy.")
        return fecha

    def clean_horaReserva(self):
        hora = self.cleaned_data['horaReserva']
        if hora < time(9, 0) or hora > time(19, 0):
            raise forms.ValidationError("La hora debe estar entre las 09:00 y las 19:00.")
        return hora

    def clean_fotoVehiculo(self):
        foto = self.cleaned_data.get('fotoVehiculo')

        if foto:
            try:
                imagen = Image.open(foto)
                imagen.verify()
                foto.seek(0)
            except Exception:
                raise forms.ValidationError(
                    "Debes seleccionar un archivo de imagen válido."
                )

        return foto

    def clean(self):
        cleaned_data = super().clean()

        fecha = cleaned_data.get('fechaReserva')
        hora = cleaned_data.get('horaReserva')

        if fecha and hora:
            nueva_inicio = datetime.combine(fecha, hora)
            nueva_fin = nueva_inicio + timedelta(hours=3)

            reservas = Ingreso.objects.filter(
                fechaReserva=fecha
            )

            for reserva in reservas:
                if reserva.id != self.instance.id:
                    reserva_inicio = datetime.combine(
                        reserva.fechaReserva,
                        reserva.horaReserva
                    )

                    reserva_fin = reserva_inicio + timedelta(hours=3)

                    if (nueva_inicio < reserva_fin and
                            nueva_fin > reserva_inicio):
                        raise forms.ValidationError(
                            "Ese horario no está disponible. "
                            "La reserva ocupa tres horas. "
                            "Selecciona otro horario."
                        )

        return cleaned_data


class FormRegistroCliente(forms.Form):
    nombre = forms.CharField(
        max_length=50,
        min_length=3,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Juan',
            'autocomplete': 'given-name'
        })
    )
    apellido = forms.CharField(
        max_length=50,
        min_length=2,
        required=True,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Pérez',
            'autocomplete': 'family-name'
        })
    )
    email = forms.EmailField(
        max_length=50,
        required=True,
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ejemplo@email.com',
            'autocomplete': 'email'
        })
    )
    telefono = forms.CharField(
        max_length=9,
        min_length=9,
        required=True,
        label="Teléfono (9 dígitos)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 912345678',
            'pattern': '[0-9]{9}',
            'title': 'Debe contener exactamente 9 dígitos numéricos'
        })
    )
    direccion = forms.CharField(
        max_length=60,
        min_length=8,
        required=True,
        label="Dirección",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Avenida Siempre Viva 123, Maipú'
        })
    )
    password = forms.CharField(
        min_length=8,
        required=True,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Crea tu contraseña segura',
            'autocomplete': 'new-password'
        })
    )
    password_confirm = forms.CharField(
        min_length=8,
        required=True,
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite tu contraseña',
            'autocomplete': 'new-password'
        })
    )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido', '').strip()
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', apellido):
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")
        return apellido

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con este correo electrónico.")
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        if len(telefono) != 9:
            raise forms.ValidationError("El teléfono debe tener exactamente 9 dígitos.")
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if len(direccion) < 8 or len(direccion) > 60:
            raise forms.ValidationError("La dirección debe tener entre 8 y 60 caracteres.")
        return direccion

    def clean_password(self):
        password = self.cleaned_data.get('password', '')

        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula.")

        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")

        if not re.search(r'[^a-zA-Z0-9]', password):
            raise forms.ValidationError(
                "La contraseña debe contener al menos un carácter especial (ej: ! @ # $ % * ? . - _)."
            )

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")

        return cleaned_data


class FormLoginCliente(forms.Form):
    identificador = forms.CharField(
        max_length=100,
        required=True,
        label="Correo o Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo o usuario',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        required=True,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password'
        })
    )
