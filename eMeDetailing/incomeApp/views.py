from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from .models import Ingreso, PerfilCliente, Servicio
from .forms import FormIngreso, FormRegistroCliente, FormLoginCliente


def _inicializar_servicios_base():
    """Crea los 3 servicios base en MySQL si aún no existen."""
    try:
        if not Servicio.objects.exists():
            Servicio.objects.create(
                nombre="Express",
                descripcion="Aspirado, Lavado exterior, Vidrios, Ruedas, Gomas",
                precio_citycar=13000,
                precio_sedan=16000,
                precio_suv=19000
            )
            Servicio.objects.create(
                nombre="Full",
                descripcion="Express + Limpieza de marcos de puertas y Encerado",
                precio_citycar=19000,
                precio_sedan=24000,
                precio_suv=29000
            )
            Servicio.objects.create(
                nombre="Full Detallado",
                descripcion="Detallado profundo, descontaminado y productos premium Meguiar’s",
                precio_citycar=29000,
                precio_sedan=34000,
                precio_suv=39000
            )
    except Exception:
        pass


def index(request):
    _inicializar_servicios_base()

    initial_data = {}
    if request.user.is_authenticated:
        perfil = getattr(request.user, 'perfil', None)
        nombre_completo = f"{request.user.first_name} {request.user.last_name}".strip()
        initial_data = {
            'nombre': nombre_completo or request.user.username,
            'email': request.user.email,
            'telefono': perfil.telefono if perfil else '',
            'direccion': perfil.direccion if perfil else '',
        }

    form = FormIngreso(initial=initial_data)

    if request.method == 'POST':
        # Requerimiento 6: Solo clientes autenticados pueden ejecutar el proceso
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para realizar una reserva.")
            return redirect('login')

        form = FormIngreso(request.POST, request.FILES)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = request.user

            # Requerimiento 3: Vinculación con la tabla Servicio (3 tablas relacionadas)
            servicio_obj = Servicio.objects.filter(nombre__iexact=reserva.servicio).first()
            if servicio_obj:
                reserva.servicio_fk = servicio_obj

            reserva.save()
            messages.success(
                request,
                "¡Tu reserva ha sido confirmada con éxito! Puedes revisar su estado a continuación."
            )
            return redirect('mis_reservas')

    servicios = Servicio.objects.all()
    return render(request, 'index.html', {'form': form, 'servicios': servicios})


# Requerimiento 7: Consultar los resultados de las operaciones realizadas (Historial / Mis Reservas)
def mis_reservas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para consultar tus reservas.")
        return redirect('login')

    reservas = Ingreso.objects.filter(cliente=request.user).order_by('-fechaReserva', '-horaReserva')
    return render(request, 'mis_reservas.html', {'reservas': reservas})


def cancelar_reserva(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    reserva = get_object_or_404(Ingreso, id=id, cliente=request.user)
    if reserva.estado == 'Pendiente':
        reserva.estado = 'Cancelada'
        reserva.save()
        messages.success(request, f"La reserva #{reserva.id} ha sido cancelada exitosamente.")
    else:
        messages.error(request, "Solo puedes cancelar reservas en estado Pendiente.")

    return redirect('mis_reservas')


def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('/')

    form_login = FormLoginCliente()
    form_registro = FormRegistroCliente()

    if request.method == 'POST':
        form_login = FormLoginCliente(request.POST)
        if form_login.is_valid():
            identificador = form_login.cleaned_data['identificador'].strip()
            password = form_login.cleaned_data['password']

            user_obj = User.objects.filter(
                models.Q(email__iexact=identificador) | models.Q(username__iexact=identificador)
            ).first()

            username_to_auth = user_obj.username if user_obj else identificador
            user = authenticate(request, username=username_to_auth, password=password)

            if user is not None:
                login(request, user)
                messages.success(
                    request,
                    f"¡Hola de nuevo, {user.first_name or user.username}! Ahora puedes reservar tu servicio."
                )
                next_url = request.GET.get('next') or '/'
                return redirect(next_url)
            else:
                messages.error(request, "Correo o contraseña incorrectos. Por favor, verifica tus datos.")

    return render(request, 'auth.html', {
        'active_tab': 'login',
        'form_login': form_login,
        'form_registro': form_registro,
    })


def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('/')

    form_login = FormLoginCliente()
    form_registro = FormRegistroCliente()

    if request.method == 'POST':
        form_registro = FormRegistroCliente(request.POST)
        if form_registro.is_valid():
            nombre = form_registro.cleaned_data['nombre']
            apellido = form_registro.cleaned_data['apellido']
            email = form_registro.cleaned_data['email']
            telefono = form_registro.cleaned_data['telefono']
            direccion = form_registro.cleaned_data['direccion']
            password = form_registro.cleaned_data['password']

            # Crear Usuario de Django (auth_user)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido
            )

            # Crear PerfilCliente relacionado
            PerfilCliente.objects.create(
                user=user,
                telefono=telefono,
                direccion=direccion,
                es_cliente=True
            )

            # Iniciar sesión automáticamente
            user_auth = authenticate(request, username=email, password=password)
            if user_auth is not None:
                login(request, user_auth)

            messages.success(
                request,
                f"¡Bienvenido a Eme Detailing, {nombre}! Tu cuenta ha sido creada exitosamente. Ya puedes realizar tu reserva."
            )
            return redirect('/')
        else:
            messages.error(request, "Por favor corrige los errores señalados en el formulario de registro.")

    return render(request, 'auth.html', {
        'active_tab': 'registro',
        'form_login': form_login,
        'form_registro': form_registro,
    })


def logout_usuario(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente. ¡Vuelve pronto!")
    return redirect('/')


# Vistas de Administración (Staff)
def listadoIngreso(request):
    if not request.user.is_staff:
        return redirect('/admin/login/')
    ingresos = Ingreso.objects.all().order_by('-id')
    data = {'ingresos': ingresos, 'totalReservas': ingresos.count()}
    return render(request, 'ingresos.html', data)


def agregarIngreso(request):
    if not request.user.is_staff:
        return redirect('/admin/login/')
    form = FormIngreso()
    if request.method == 'POST':
        form = FormIngreso(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/ingresos/')

    return render(request, 'agregar.html', {'form': form})


def eliminarIngreso(request, id):
    if not request.user.is_staff:
        return redirect('/admin/login/')
    ingreso = get_object_or_404(Ingreso, id=id)
    if request.method == 'POST':
        ingreso.delete()
        return redirect('/ingresos/')
    return render(request, 'eliminar.html', {'ingreso': ingreso})


def actualizarIngreso(request, id):
    if not request.user.is_staff:
        return redirect('/admin/login/')
    ingreso = get_object_or_404(Ingreso, id=id)
    form = FormIngreso(instance=ingreso)
    if request.method == 'POST':
        form = FormIngreso(request.POST, request.FILES, instance=ingreso)
        if form.is_valid():
            form.save()
            return redirect('/ingresos/')

    return render(request, 'actualizar.html', {'form': form})
