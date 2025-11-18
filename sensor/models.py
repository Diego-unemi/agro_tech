from django.db import models
from farms.models import Zona

class Sensor(models.Model):
    TIPO_CHOICES = [
        ('TEMPERATURA', 'Sensor de Temperatura'),
        ('HUMEDAD', 'Sensor de Humedad'),
        ('CO2', 'Sensor de CO2'),
        ('MULTIFUNCION', 'Sensor Multifunción'),
    ]
    
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('ERROR', 'Con Error'),
    ]
    
    nombre = models.CharField('Nombre del Sensor', max_length=200)
    codigo_serial = models.CharField('Código Serial', max_length=100, unique=True)
    tipo = models.CharField('Tipo de Sensor', max_length=20, choices=TIPO_CHOICES)
    zona = models.ForeignKey(
        Zona,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores',
        verbose_name='Zona Asignada'
    )
    estado = models.CharField('Estado', max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    fecha_instalacion = models.DateField('Fecha de Instalación', null=True, blank=True)
    ultima_lectura = models.DateTimeField('Última Lectura', null=True, blank=True)
    descripcion = models.TextField('Descripción', blank=True)
    fabricante = models.CharField('Fabricante', max_length=200, blank=True)
    modelo = models.CharField('Modelo', max_length=200, blank=True)
    fecha_registro = models.DateTimeField('Fecha de Registro', auto_now_add=True)
    ultima_modificacion = models.DateTimeField('Última Modificación', auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo_serial})"
    
    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'
        ordering = ['-fecha_registro']
    
    def actualizar_ultima_lectura(self):
        """Actualiza el timestamp de la última lectura"""
        from django.utils import timezone
        self.ultima_lectura = timezone.now()
        self.save(update_fields=['ultima_lectura'])
    
    def esta_activo(self):
        """Verifica si el sensor está activo y puede enviar datos"""
        return self.estado == 'ACTIVO'
