
from django.db import models


class Ingreso(models.Model):


    servicio = models.CharField(max_length=20 )
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    telefono = models.CharField(max_length=9)
    vehiculo = models.CharField(max_length=50,)
    direccion = models.CharField(max_length=60)
    fechaReserva = models.DateField()
    horaReserva = models.TimeField()
    fotoVehiculo = models.ImageField(
        upload_to='vehiculos/',
        null=True,
        blank=True
    )


    def __str__(self):
        return self.nombre + " - " + self.servicio

    def delete(self, *args, **kwargs):
        if self.fotoVehiculo:
            self.fotoVehiculo.delete(save=False)

        super().delete(*args, **kwargs)
