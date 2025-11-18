from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('No ingresaste una dirección de correo electrónico válida')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('AGRONOMO', 'Agrónomo'),
        ('TECNICO', 'Técnico Agrícola'),
        ('AGRICULTOR', 'Agricultor'),
    ]
    
    first_name = models.CharField('Nombres', max_length=30, blank=True)
    last_name = models.CharField('Apellidos', max_length=30, blank=True)
    email = models.EmailField('Correo Electrónico', unique=True)
    phone = models.CharField('Telefono', max_length=50, blank=True, null=True)
    role = models.CharField('Rol', max_length=20, choices=ROLE_CHOICES, default='AGRICULTOR')
    is_active = models.BooleanField('Activo', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    date_joined = models.DateTimeField('Fecha de Creación', auto_now_add=True)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser
    
    def is_agronomo(self):
        return self.role == 'AGRONOMO'
    
    def is_tecnico(self):
        return self.role == 'TECNICO'
    
    def is_agricultor(self):
        return self.role == 'AGRICULTOR'
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']
