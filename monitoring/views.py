from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sensor.models import Sensor
from alerts.models import UmbralAlerta, Alerta
import json
import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from .models import SensorData
from alerts.models import Alerta

LATEST_DATA_FILE = 'latest_sensor_data.json'

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
def obtener_unidad(parametro):
    return {
        'TEMPERATURA': '°C',
        'HUMEDAD': '%',
        'CO2': 'ppm',
    }.get(parametro, '')

@csrf_exempt
def recibir_datos(request):
    if request.method == 'POST':
        try:
            # Obtener datos del sensor
            datos = json.loads(request.body)
            codigo_serial = datos.get('codigo_serial')
            lecturas = {
                'TEMPERATURA': float(datos.get('temperature')),
                'HUMEDAD': float(datos.get('humidity')),
                'CO2': float(datos.get('co2_ppm')),
            }

            logger.info(f"Datos recibidos de {codigo_serial}: {lecturas}")

            # Buscar el sensor
            try:
                sensor = Sensor.objects.get(codigo_serial=codigo_serial)
            except Sensor.DoesNotExist:
                return JsonResponse({'error': 'Sensor no encontrado'}, status=404)

            # Verificar umbrales y crear alertas
            alertas_creadas = []
            for parametro, valor in lecturas.items():
                umbrales = UmbralAlerta.objects.filter(
                    zona=sensor.zona,
                    parametro=parametro,
                    activo=True
                )

                for umbral in umbrales:
                    alerta = None
                    if valor > umbral.valor_maximo:
                        alerta = Alerta.objects.create(
                            sensor=sensor,
                            zona=sensor.zona,
                            parametro=parametro,
                            tipo_alerta='EXCESO',
                            nivel_severidad=umbral.nivel_severidad,
                            lectura_valor=valor,
                            umbral=umbral,
                            mensaje=f'{parametro}: {valor} {obtener_unidad(parametro)} supera el umbral máximo de {umbral.valor_maximo} {obtener_unidad(parametro)}'
                        )
                    elif valor < umbral.valor_minimo:
                        alerta = Alerta.objects.create(
                            sensor=sensor,
                            zona=sensor.zona,
                            parametro=parametro,
                            tipo_alerta='DEFECTO',
                            nivel_severidad=umbral.nivel_severidad,
                            lectura_valor=valor,
                            umbral=umbral,
                            mensaje=f'{parametro}: {valor} {obtener_unidad(parametro)} por debajo del umbral mínimo de {umbral.valor_minimo} {obtener_unidad(parametro)}'
                        )
                    
                    if alerta:
                        alertas_creadas.append({
                            'parametro': parametro,
                            'valor': valor,
                            'tipo': alerta.tipo_alerta,
                            'severidad': alerta.nivel_severidad
                        })
                        logger.warning(f"Alerta creada: {alerta.mensaje}")

            return JsonResponse({
                'status': 'success',
                'data': lecturas,
                'alertas_creadas': alertas_creadas
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
        except Exception as e:
            logger.error(f"Error procesando datos: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required(login_url='/login/')
def obtener_datos(request):
    try:
        with open(LATEST_DATA_FILE, 'r') as f:
            data = json.load(f)
        return JsonResponse(data)
    except FileNotFoundError:
        return JsonResponse({
            'temperature': "N/A",
            'humidity': "N/A",
            'co2_ppm': "N/A",
        })

@login_required(login_url='/login/')
def dashboard(request):
    # Calcular fecha de inicio (últimas 24 horas)
    fecha_inicio = timezone.now() - timedelta(hours=24)
    
    # Obtener conteo de sensores activos
    sensores_activos = Sensor.objects.filter(estado='ACTIVO').count()
    
    # Obtener resumen de alertas
    alertas = Alerta.objects.filter(fecha_creacion__gte=fecha_inicio)
    resumen_alertas = {
        'total': alertas.count(),
        'nuevas': alertas.filter(estado='NUEVA').count(),
        'criticas': alertas.filter(nivel_severidad='CRITICA').count(),
    }
    
    # Datos históricos para las gráficas
    datos_historicos = SensorData.objects.filter(
        timestamp__gte=fecha_inicio
    ).values('timestamp').annotate(
        temp_promedio=Avg('temperature'),
        hum_promedio=Avg('humidity'),
        co2_promedio=Avg('co2_ppm')
    ).order_by('timestamp')

    # Convertir los datos a formato JSON serializable
    datos_graficas = [{
        'timestamp': data['timestamp'].isoformat(),
        'temp_promedio': float(data['temp_promedio']) if data['temp_promedio'] else 0,
        'hum_promedio': float(data['hum_promedio']) if data['hum_promedio'] else 0,
        'co2_promedio': float(data['co2_promedio']) if data['co2_promedio'] else 0
    } for data in datos_historicos]

    # Últimas alertas
    ultimas_alertas = Alerta.objects.filter(
        fecha_creacion__gte=fecha_inicio
    ).order_by('-fecha_creacion')[:3]

    context = {
        'sensores_activos': sensores_activos,
        'resumen_alertas': resumen_alertas,
        'datos_historicos': datos_graficas,
        'ultima_actualizacion': timezone.now(),
        'ultimas_alertas': ultimas_alertas
    }
    return render(request, 'monitoring/dashboard.html', context)

@login_required(login_url='/login/')
def obtener_datos_historicos(request):
    fecha_inicio = timezone.now() - timedelta(hours=24)
    
    datos_historicos = SensorData.objects.filter(
        timestamp__gte=fecha_inicio
    ).values('timestamp').annotate(
        temp_promedio=Avg('temperature'),
        hum_promedio=Avg('humidity'),
        co2_promedio=Avg('co2_ppm')
    ).order_by('timestamp')

    datos = [{
        'timestamp': data['timestamp'].isoformat(),
        'temp_promedio': float(data['temp_promedio']) if data['temp_promedio'] else 0,
        'hum_promedio': float(data['hum_promedio']) if data['hum_promedio'] else 0,
        'co2_promedio': float(data['co2_promedio']) if data['co2_promedio'] else 0
    } for data in datos_historicos]

    return JsonResponse(datos, safe=False)