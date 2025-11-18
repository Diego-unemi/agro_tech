from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect

def role_required(*roles):
    """
    Decorador para verificar que el usuario tiene uno de los roles requeridos.
    Uso: @role_required('ADMIN', 'AGRONOMO')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            
            raise PermissionDenied("No tienes permisos para acceder a esta página.")
        
        return wrapped_view
    return decorator

def admin_required(view_func):
    """
    Decorador para verificar que el usuario es administrador.
    Uso: @admin_required
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.is_admin():
            return view_func(request, *args, **kwargs)
        
        raise PermissionDenied("Necesitas ser administrador para acceder a esta página.")
    
    return wrapped_view

def agronomo_or_admin_required(view_func):
    """
    Decorador para verificar que el usuario es agrónomo o administrador.
    Uso: @agronomo_or_admin_required
    """
    return role_required('ADMIN', 'AGRONOMO')(view_func)

def tecnico_or_admin_required(view_func):
    """
    Decorador para verificar que el usuario es técnico o administrador.
    Uso: @tecnico_or_admin_required
    """
    return role_required('ADMIN', 'TECNICO')(view_func)

