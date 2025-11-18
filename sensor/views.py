from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Sensor
from .forms import SensorForm
from security.decorators import role_required, tecnico_or_admin_required
from farms.models import Zona

@login_required(login_url='/login/')
def sensor_list(request):
    """Vista para listar todos los sensores"""
    search_query = request.GET.get('search', '')
    tipo_filter = request.GET.get('tipo', '')
    estado_filter = request.GET.get('estado', '')
    zona_filter = request.GET.get('zona', '')
    
    sensores = Sensor.objects.select_related('zona', 'zona__finca').all()
    
    # Filtrar según usuario si no es admin
    if not request.user.is_admin():
        sensores = sensores.filter(
            Q(zona__finca__propietario=request.user) | 
            Q(zona__finca__usuarios_asignados=request.user)
        ).distinct()
    
    if search_query:
        sensores = sensores.filter(
            Q(nombre__icontains=search_query) | 
            Q(codigo_serial__icontains=search_query) | 
            Q(fabricante__icontains=search_query) | 
            Q(modelo__icontains=search_query)
        )
    
    if tipo_filter:
        sensores = sensores.filter(tipo=tipo_filter)
    
    if estado_filter:
        sensores = sensores.filter(estado=estado_filter)
    
    if zona_filter:
        sensores = sensores.filter(zona_id=zona_filter)
    
    paginator = Paginator(sensores, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener zonas para el filtro
    if request.user.is_admin():
        zonas = Zona.objects.select_related('finca').all()
    else:
        zonas = Zona.objects.filter(
            Q(finca__propietario=request.user) | 
            Q(finca__usuarios_asignados=request.user)
        ).distinct().select_related('finca')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'tipo_filter': tipo_filter,
        'estado_filter': estado_filter,
        'zona_filter': zona_filter,
        'tipo_choices': Sensor.TIPO_CHOICES,
        'estado_choices': Sensor.ESTADO_CHOICES,
        'zonas': zonas,
    }
    return render(request, 'sensor/sensor_list.html', context)

@tecnico_or_admin_required
def sensor_create(request):
    """Vista para crear un nuevo sensor"""
    if request.method == 'POST':
        form = SensorForm(request.POST, user=request.user)
        if form.is_valid():
            sensor = form.save()
            messages.success(request, f'Sensor "{sensor.nombre}" creado exitosamente.')
            return redirect('sensor_detail', sensor_id=sensor.id)
    else:
        form = SensorForm(user=request.user)
    
    return render(request, 'sensor/sensor_form.html', {
        'form': form,
        'title': 'Registrar Nuevo Sensor',
        'button_text': 'Registrar Sensor'
    })

@login_required(login_url='/login/')
def sensor_detail(request, sensor_id):
    """Vista para ver detalle de un sensor"""
    sensor = get_object_or_404(Sensor, id=sensor_id)
    
    # Verificar acceso si el sensor tiene zona asignada
    if sensor.zona:
        if not sensor.zona.tiene_acceso(request.user):
            messages.error(request, 'No tienes permisos para ver este sensor.')
            return redirect('sensor_list')
    elif not request.user.is_admin():
        messages.error(request, 'No tienes permisos para ver este sensor.')
        return redirect('sensor_list')
    
    context = {
        'sensor': sensor,
    }
    return render(request, 'sensor/sensor_detail.html', context)

@tecnico_or_admin_required
def sensor_edit(request, sensor_id):
    """Vista para editar un sensor"""
    sensor = get_object_or_404(Sensor, id=sensor_id)
    
    # Verificar permisos
    if sensor.zona and not request.user.is_admin():
        if not (request.user == sensor.zona.finca.propietario or 
                request.user in sensor.zona.finca.usuarios_asignados.all()):
            messages.error(request, 'No tienes permisos para editar este sensor.')
            return redirect('sensor_detail', sensor_id=sensor.id)
    
    if request.method == 'POST':
        form = SensorForm(request.POST, instance=sensor, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sensor "{sensor.nombre}" actualizado exitosamente.')
            return redirect('sensor_detail', sensor_id=sensor.id)
    else:
        form = SensorForm(instance=sensor, user=request.user)
    
    return render(request, 'sensor/sensor_form.html', {
        'form': form,
        'sensor': sensor,
        'title': 'Editar Sensor',
        'button_text': 'Guardar Cambios'
    })

@role_required('ADMIN', 'TECNICO')
def sensor_delete(request, sensor_id):
    """Vista para eliminar un sensor"""
    sensor = get_object_or_404(Sensor, id=sensor_id)
    
    if request.method == 'POST':
        nombre = sensor.nombre
        sensor.delete()
        messages.success(request, f'Sensor "{nombre}" eliminado exitosamente.')
        return redirect('sensor_list')
    
    return render(request, 'sensor/sensor_confirm_delete.html', {'sensor': sensor})

# Vista legacy para compatibilidad
@login_required(login_url='/login/')
def sensor_config(request):
    """Redirección a la nueva vista de listado"""
    return redirect('sensor_list')
