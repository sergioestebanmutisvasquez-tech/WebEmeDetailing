from django import forms
from datetime import datetime, timedelta, date, time
from .models import Ingreso
from PIL import Image


class FormIngreso(forms.ModelForm):

    class Meta:
        model = Ingreso
        fields = '__all__'

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
       if  fecha < date.today():
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
