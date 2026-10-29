from django.contrib import admin
from .models import Ingreso
from .forms import FormIngreso

# Register your models here.
class IngresoAdmin(admin.ModelAdmin):
    form = FormIngreso
    list_display = ['servicio','nombre','email','telefono','vehiculo','direccion','fechaReserva','horaReserva','fotoVehiculo']

admin.site.register(Ingreso,IngresoAdmin)
