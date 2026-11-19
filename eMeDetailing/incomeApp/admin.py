from django.contrib import admin
from .models import Ingreso, PerfilCliente, Servicio
from .forms import FormIngreso


class PerfilClienteAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono', 'direccion', 'es_cliente']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'telefono']
    list_filter = ['es_cliente']


class ServicioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio_citycar', 'precio_sedan', 'precio_suv']
    search_fields = ['nombre']


class IngresoAdmin(admin.ModelAdmin):
    form = FormIngreso
    list_display = [
        'id', 'servicio', 'nombre', 'cliente', 'telefono',
        'vehiculo', 'direccion', 'fechaReserva', 'horaReserva', 'estado'
    ]
    search_fields = ['nombre', 'email', 'telefono', 'servicio']
    list_filter = ['estado', 'servicio', 'vehiculo', 'fechaReserva']
    list_editable = ['estado']


admin.site.register(PerfilCliente, PerfilClienteAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Ingreso, IngresoAdmin)
