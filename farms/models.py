from django.db import models
from django.conf import settings

class Finca(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('INACTIVA', 'Inactiva'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
    ]
    
    nombre = models.CharField('Nombre de la Finca', max_length=200)
    ubicacion = models.CharField('Ubicación', max_length=300, help_text='Ciudad, provincia o coordenadas')
    direccion = models.TextField('Dirección', blank=True)
    area_total = models.DecimalField('Área Total (hectáreas)', max_digits=10, decimal_places=2)
    cultivo_actual = models.CharField('Cultivo Actual', max_length=200)
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='fincas_propias',
        verbose_name='Propietario'
    )
    usuarios_asignados = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='fincas_asignadas',
        blank=True,
        verbose_name='Usuarios Asignados',
        help_text='Usuarios que tienen acceso a esta finca'
    )
    estado = models.CharField('Estado', max_length=20, choices=ESTADO_CHOICES, default='ACTIVA')
    fecha_registro = models.DateTimeField('Fecha de Registro', auto_now_add=True)
    ultima_modificacion = models.DateTimeField('Última Modificación', auto_now=True)
    notas = models.TextField('Notas', blank=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"
    
    class Meta:
        verbose_name = 'Finca'
        verbose_name_plural = 'Fincas'
        ordering = ['-fecha_registro']
    
    def get_usuarios_asignados_display(self):
        """Retorna lista de nombres de usuarios asignados"""
        return ", ".join([u.get_full_name() for u in self.usuarios_asignados.all()])
    
    def tiene_acceso(self, usuario):
        """Verifica si un usuario tiene acceso a esta finca"""
        return (
            usuario.is_admin() or 
            usuario == self.propietario or 
            usuario in self.usuarios_asignados.all()
        )


class Zona(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('INACTIVA', 'Inactiva'),
        ('PREPARACION', 'En Preparación'),
        ('COSECHA', 'En Cosecha'),
    ]
    
    nombre = models.CharField('Nombre de la Zona', max_length=200)
    finca = models.ForeignKey(
        Finca,
        on_delete=models.CASCADE,
        related_name='zonas',
        verbose_name='Finca'
    )
    tipo_cultivo = models.CharField('Tipo de Cultivo', max_length=200)
    area = models.DecimalField('Área (hectáreas)', max_digits=10, decimal_places=2)
    descripcion = models.TextField('Descripción', blank=True)
    coordenadas = models.JSONField('Coordenadas', blank=True, null=True, help_text='Coordenadas GPS para mapeo')
    estado = models.CharField('Estado', max_length=20, choices=ESTADO_CHOICES, default='ACTIVA')
    fecha_creacion = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    ultima_modificacion = models.DateTimeField('Última Modificación', auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.finca.nombre}"
    
    class Meta:
        verbose_name = 'Zona de Cultivo'
        verbose_name_plural = 'Zonas de Cultivo'
        ordering = ['finca', 'nombre']
        unique_together = ['finca', 'nombre']
    
    def tiene_acceso(self, usuario):
        """Verifica si un usuario tiene acceso a esta zona (heredado de la finca)"""
        return self.finca.tiene_acceso(usuario)
