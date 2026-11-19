"""
URL configuration for registroClientes project.
"""
from django.contrib import admin
from django.urls import path
from incomeApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_usuario, name='login'),
    path('registro/', views.registro_usuario, name='registro'),
    path('logout/', views.logout_usuario, name='logout'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar-reserva/<int:id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('ingresos/', views.listadoIngreso, name='listado_ingreso'),
    path('agregar/', views.agregarIngreso, name='agregar_ingreso'),
    path('eliminar/<int:id>/', views.eliminarIngreso, name='eliminar_ingreso'),
    path('actualizar/<int:id>/', views.actualizarIngreso, name='actualizar_ingreso'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
