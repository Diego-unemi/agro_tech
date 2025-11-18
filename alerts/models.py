from django.db import models
from sensor.models import Sensor
from farms.models import Zona

class UmbralAlerta(models.Model):
    PARAMETROS_CHOICES = [
        ('TEMPERATURA', 'Temperatura'),
        ('HUMEDAD', 'Humedad'),
        ('CO2', 'CO2'),
    ]
    
    SEVERIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    parametro = models.CharField(max_length=20, choices=PARAMETROS_CHOICES)
    valor_minimo = models.FloatField()
    valor_maximo = models.FloatField()
    nivel_severidad = models.CharField(max_length=10, choices=SEVERIDAD_CHOICES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.zona} - {self.parametro} ({self.nivel_severidad})"

class Alerta(models.Model):
    ESTADO_CHOICES = [
        ('NUEVA', 'Nueva'),
        ('LEIDA', 'Leída'),
        ('RESUELTA', 'Resuelta'),
    ]

    sensor = models.ForeignKey(
        Sensor, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    zona = models.ForeignKey(
        Zona, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    parametro = models.CharField(max_length=20)
    tipo_alerta = models.CharField(max_length=10)  # EXCESO o DEFECTO
    nivel_severidad = models.CharField(max_length=10)
    lectura_valor = models.FloatField()
    umbral = models.ForeignKey(
        UmbralAlerta, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='NUEVA'
    )

    def __str__(self):
        return f"{self.parametro} - {self.tipo_alerta} ({self.fecha_creacion})"

    class Meta:
        ordering = ['-fecha_creacion']

    def resolver(self):
        self.estado = 'RESUELTA'
        self.save()
