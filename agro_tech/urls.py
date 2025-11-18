"""
URL configuration for agro_tech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from security import views as security_views
from monitoring import views as monitoring_views
from core import views as core_views
from sensor import views as sensor_views
from farms import views as farms_views
from alerts import views as alerts_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.base, name='base'),
    path('dashboard/', monitoring_views.dashboard, name='dashboard'),
    
    # Autenticación
    path('registro/', security_views.registro, name='registro'),
    path('login/', security_views.user_login, name='login'),
    path('logout/', security_views.user_logout, name='logout'),
    path('success/', security_views.success, name='success'),
    
    # Gestión de Usuarios
    path('usuarios/', security_views.user_list, name='user_list'),
    path('usuarios/crear/', security_views.user_create, name='user_create'),
    path('usuarios/<int:user_id>/editar/', security_views.user_edit, name='user_edit'),
    path('usuarios/<int:user_id>/eliminar/', security_views.user_delete, name='user_delete'),
    path('perfil/', security_views.user_profile, name='user_profile'),
    
    # Monitoreo
    path('recibir_datos/', monitoring_views.recibir_datos, name='recibir_datos'),
    path('obtener_datos/', monitoring_views.obtener_datos, name='obtener_datos'),
    path('obtener_datos_historicos/', monitoring_views.obtener_datos_historicos, name='obtener_datos_historicos'),
    
    # Sensores
    path('sensores/', sensor_views.sensor_list, name='sensor_list'),
    path('sensores/crear/', sensor_views.sensor_create, name='sensor_create'),
    path('sensores/<int:sensor_id>/', sensor_views.sensor_detail, name='sensor_detail'),
    path('sensores/<int:sensor_id>/editar/', sensor_views.sensor_edit, name='sensor_edit'),
    path('sensores/<int:sensor_id>/eliminar/', sensor_views.sensor_delete, name='sensor_delete'),
    path('sensor/', sensor_views.sensor_config, name='sensor'),  # Legacy route
    
    # Fincas
    path('fincas/', farms_views.finca_list, name='finca_list'),
    path('fincas/crear/', farms_views.finca_create, name='finca_create'),
    path('fincas/<int:finca_id>/', farms_views.finca_detail, name='finca_detail'),
    path('fincas/<int:finca_id>/editar/', farms_views.finca_edit, name='finca_edit'),
    path('fincas/<int:finca_id>/eliminar/', farms_views.finca_delete, name='finca_delete'),
    path('finca/', farms_views.finca, name='finca'),  # Legacy route
    
    # Zonas
    path('fincas/<int:finca_id>/zonas/crear/', farms_views.zona_create, name='zona_create'),
    path('zonas/<int:zona_id>/editar/', farms_views.zona_edit, name='zona_edit'),
    path('zonas/<int:zona_id>/eliminar/', farms_views.zona_delete, name='zona_delete'),
    
    # Umbrales y Alertas
    path('umbrales/', alerts_views.umbral_list, name='umbral_list'),
    path('umbrales/crear/', alerts_views.umbral_create, name='umbral_create'),
    path('umbrales/<int:umbral_id>/editar/', alerts_views.umbral_edit, name='umbral_edit'),
    path('umbrales/<int:umbral_id>/eliminar/', alerts_views.umbral_delete, name='umbral_delete'),
    path('alertas/', alerts_views.alerta_list, name='alerta_list'),
    path('alertas/<int:alerta_id>/resolver/', alerts_views.alerta_resolver, name='alerta_resolver'),
]
