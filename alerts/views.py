from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import UmbralAlerta, Alerta
from .forms import UmbralAlertaForm
from security.decorators import agronomo_or_admin_required, role_required
from farms.models import Zona
from alerts.models import UmbralAlerta, Alerta
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sensor.models import Sensor
from alerts.models import UmbralAlerta, Alerta
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def recibir_datos(request):
    if request.method == 'POST':
        try:
            # Obtener datos del request
            datos = json.loads(request.body)
            codigo_serial = datos.get('codigo_serial')
            temperatura = float(datos.get('temperatura'))
            humedad = float(datos.get('humedad'))
            
            logger.debug(f"Datos recibidos - Serial: {codigo_serial}, Temp: {temperatura}°C, Hum: {humedad}%")

            # Buscar el sensor por código serial
            try:
                sensor = Sensor.objects.get(codigo_serial=codigo_serial)
            except Sensor.DoesNotExist:
                return JsonResponse({'error': 'Sensor no encontrado'}, status=404)

            # Verificar umbrales de temperatura
            umbrales_temp = UmbralAlerta.objects.filter(
                zona=sensor.zona,
                parametro='TEMPERATURA'
            )

            for umbral in umbrales_temp:
                if temperatura > umbral.valor_maximo:
                    Alerta.objects.create(
                        sensor=sensor,
                        zona=sensor.zona,
                        parametro='TEMPERATURA',
                        tipo_alerta='EXCESO',
                        nivel_severidad=umbral.nivel_severidad,
                        lectura_valor=temperatura,
                        umbral=umbral,
                        mensaje=f'Temperatura {temperatura}°C supera el umbral máximo de {umbral.valor_maximo}°C'
                    )
                    logger.warning(f"Alerta creada: temperatura alta {temperatura}°C")

                elif temperatura < umbral.valor_minimo:
                    Alerta.objects.create(
                        sensor=sensor,
                        zona=sensor.zona,
                        parametro='TEMPERATURA',
                        tipo_alerta='DEFECTO',
                        nivel_severidad=umbral.nivel_severidad,
                        lectura_valor=temperatura,
                        umbral=umbral,
                        mensaje=f'Temperatura {temperatura}°C por debajo del umbral mínimo de {umbral.valor_minimo}°C'
                    )
                    logger.warning(f"Alerta creada: temperatura baja {temperatura}°C")

            # Similar para humedad...

            return JsonResponse({'status': 'success'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
        except Exception as e:
            logger.error(f"Error procesando datos: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required(login_url='/login/')
def umbral_list(request):
    # Obtener filtros
    zona_filter = request.GET.get('zona')
    parametro_filter = request.GET.get('parametro')
    
    # Consulta base
    umbrales = UmbralAlerta.objects.all()
    
    # Aplicar filtros si existen
    if zona_filter:
        umbrales = umbrales.filter(zona_id=zona_filter)
    if parametro_filter:
        umbrales = umbrales.filter(parametro=parametro_filter)
    
    # Paginación
    paginator = Paginator(umbrales, 10)  # 10 items por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Preparar contexto
    context = {
        'page_obj': page_obj,
        'zonas': Zona.objects.all(),
        'parametro_choices': UmbralAlerta.PARAMETROS_CHOICES,  # Corregido aquí
        'zona_filter': zona_filter,
        'parametro_filter': parametro_filter,
    }
    
    return render(request, 'alerts/umbral_list.html', context)

@agronomo_or_admin_required
def umbral_create(request):
    """Vista para crear un nuevo umbral"""
    if request.method == 'POST':
        form = UmbralAlertaForm(request.POST)
        if form.is_valid():
            umbral = form.save(commit=False)
            umbral.creado_por = request.user
            umbral.save()
            messages.success(request, f'Umbral para {umbral.get_parametro_display()} en {umbral.zona.nombre} creado exitosamente.')
            return redirect('umbral_list')
    else:
        form = UmbralAlertaForm()
    
    return render(request, 'alerts/umbral_form.html', {
        'form': form,
        'title': 'Crear Umbral de Alerta',
        'button_text': 'Crear Umbral'
    })

@agronomo_or_admin_required
def umbral_edit(request, umbral_id):
    """Vista para editar un umbral"""
    umbral = get_object_or_404(UmbralAlerta, id=umbral_id)
    
    if request.method == 'POST':
        form = UmbralAlertaForm(request.POST, instance=umbral)
        if form.is_valid():
            form.save()
            messages.success(request, f'Umbral actualizado exitosamente.')
            return redirect('umbral_list')
    else:
        form = UmbralAlertaForm(instance=umbral)
    
    return render(request, 'alerts/umbral_form.html', {
        'form': form,
        'umbral': umbral,
        'title': 'Editar Umbral',
        'button_text': 'Guardar Cambios'
    })

@role_required('ADMIN', 'AGRONOMO')
def umbral_delete(request, umbral_id):
    """Vista para eliminar un umbral"""
    umbral = get_object_or_404(UmbralAlerta, id=umbral_id)
    
    if request.method == 'POST':
        umbral.delete()
        messages.success(request, 'Umbral eliminado exitosamente.')
        return redirect('umbral_list')
    
    return render(request, 'alerts/umbral_confirm_delete.html', {'umbral': umbral})

@login_required(login_url='/login/')
def alerta_list(request):
    """Vista para listar alertas"""
    estado_filter = request.GET.get('estado', '')
    zona_filter = request.GET.get('zona', '')
    
    alertas = Alerta.objects.select_related('zona', 'zona__finca', 'sensor', 'umbral').all()
    
    # Filtrar según usuario si no es admin
    if not request.user.is_admin():
        alertas = alertas.filter(
            Q(zona__finca__propietario=request.user) | 
            Q(zona__finca__usuarios_asignados=request.user)
        ).distinct()
    
    if estado_filter:
        alertas = alertas.filter(estado=estado_filter)
    
    if zona_filter:
        alertas = alertas.filter(zona_id=zona_filter)
    
    paginator = Paginator(alertas, 20)
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
        'estado_filter': estado_filter,
        'zona_filter': zona_filter,
        'estado_choices': Alerta.ESTADO_CHOICES,
        'zonas': zonas,
    }
    return render(request, 'alerts/alerta_list.html', context)

@login_required(login_url='/login/')
def alerta_resolver(request, alerta_id):
    """Vista para resolver una alerta"""
    alerta = get_object_or_404(Alerta, id=alerta_id)
    
    if not alerta.zona.tiene_acceso(request.user):
        messages.error(request, 'No tienes permisos para resolver esta alerta.')
        return redirect('alerta_list')
    
    alerta.resolver()
    messages.success(request, 'Alerta resuelta.')
    return redirect('alerta_list')
