from django.contrib import admin
from .models import Sensor

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo_serial', 'tipo', 'zona', 'estado', 'ultima_lectura', 'fecha_instalacion']
    list_filter = ['tipo', 'estado', 'zona__finca', 'fecha_instalacion']
    search_fields = ['nombre', 'codigo_serial', 'fabricante', 'modelo']
    readonly_fields = ['fecha_registro', 'ultima_modificacion', 'ultima_lectura']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo_serial', 'tipo', 'fabricante', 'modelo', 'descripcion')
        }),
        ('Asignación y Estado', {
            'fields': ('zona', 'estado', 'fecha_instalacion')
        }),
        ('Información de Sistema', {
            'fields': ('ultima_lectura', 'fecha_registro', 'ultima_modificacion')
        }),
    )
