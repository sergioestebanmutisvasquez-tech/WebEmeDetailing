from django.shortcuts import render, redirect, get_object_or_404
from .models import Ingreso
from .forms import FormIngreso

# Create your views here.

def index(request):
    form = FormIngreso()
    if request.method == 'POST':
        form = FormIngreso(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'index.html', {'form': form})

def listadoIngreso(request):
    if not request.user.is_staff:
        return redirect('/admin/login/')
    ingresos = Ingreso.objects.all().order_by('-id')
    data ={'ingresos': ingresos,'totalReservas': ingresos.count()}
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




