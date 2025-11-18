from django.contrib import admin
from .models import UmbralAlerta, Alerta

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = [
        'sensor',
        'zona',
        'parametro',
        'tipo_alerta',
        'nivel_severidad',
        'lectura_valor',
        'fecha_creacion',
        'leida'
    ]
    list_filter = [
        'zona',
        'parametro',
        'nivel_severidad',
        'leida'
    ]
    search_fields = ['sensor__codigo_serial', 'zona__nombre']
    readonly_fields = [
        'sensor',
        'zona',
        'parametro',
        'tipo_alerta',
        'nivel_severidad',
        'lectura_valor',
        'umbral',
        'mensaje',
        'fecha_creacion'
    ]

@admin.register(UmbralAlerta)
class UmbralAlertaAdmin(admin.ModelAdmin):
    list_display = [
        'zona',
        'parametro',
        'valor_minimo',
        'valor_maximo',
        'nivel_severidad',
        'activo'
    ]
    list_filter = [
        'zona',
        'parametro',
        'nivel_severidad',
        'activo'
    ]
    search_fields = ['zona__nombre']
