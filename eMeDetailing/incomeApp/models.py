from django.db import models
from django.contrib.auth.models import User


class PerfilCliente(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuario'
    )
    telefono = models.CharField(max_length=9, verbose_name='Teléfono')
    direccion = models.CharField(max_length=60, verbose_name='Dirección')
    es_cliente = models.BooleanField(default=True, verbose_name='Es Cliente')

    class Meta:
        verbose_name = 'Perfil de Cliente'
        verbose_name_plural = 'Perfiles de Clientes'

    def __str__(self):
        nombre_completo = f"{self.user.first_name} {self.user.last_name}".strip()
        return nombre_completo if nombre_completo else self.user.username


class Servicio(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre del servicio')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    precio_citycar = models.IntegerField(default=13000, verbose_name='Precio Citycar')
    precio_sedan = models.IntegerField(default=16000, verbose_name='Precio Sedan')
    precio_suv = models.IntegerField(default=19000, verbose_name='Precio SUV')

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre


class Ingreso(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Realizada', 'Realizada'),
        ('Cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservas',
        verbose_name='Cliente registrado'
    )
    servicio_fk = models.ForeignKey(
        Servicio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservas',
        verbose_name='Servicio'
    )
    servicio = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    telefono = models.CharField(max_length=9)
    vehiculo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=60)
    fechaReserva = models.DateField()
    horaReserva = models.TimeField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Pendiente',
        verbose_name='Estado de la reserva'
    )
    fotoVehiculo = models.ImageField(
        upload_to='vehiculos/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} - {self.servicio} ({self.fechaReserva})"

    def delete(self, *args, **kwargs):
        if self.fotoVehiculo:
            self.fotoVehiculo.delete(save=False)

        super().delete(*args, **kwargs)
