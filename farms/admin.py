from django.contrib import admin
from .models import Finca, Zona

@admin.register(Finca)
class FincaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'area_total', 'cultivo_actual', 'propietario', 'estado', 'fecha_registro']
    list_filter = ['estado', 'fecha_registro', 'cultivo_actual']
    search_fields = ['nombre', 'ubicacion', 'cultivo_actual', 'propietario__email']
    filter_horizontal = ['usuarios_asignados']
    readonly_fields = ['fecha_registro', 'ultima_modificacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'ubicacion', 'direccion', 'area_total', 'cultivo_actual')
        }),
        ('Gestión', {
            'fields': ('propietario', 'usuarios_asignados', 'estado')
        }),
        ('Información Adicional', {
            'fields': ('notas', 'fecha_registro', 'ultima_modificacion')
        }),
    )

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'finca', 'tipo_cultivo', 'area', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'finca', 'tipo_cultivo']
    search_fields = ['nombre', 'tipo_cultivo', 'finca__nombre']
    readonly_fields = ['fecha_creacion', 'ultima_modificacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('finca', 'nombre', 'tipo_cultivo', 'area', 'descripcion')
        }),
        ('Estado y Ubicación', {
            'fields': ('estado', 'coordenadas')
        }),
        ('Información de Sistema', {
            'fields': ('fecha_creacion', 'ultima_modificacion')
        }),
    )
