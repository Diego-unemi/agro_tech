from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Finca, Zona
from .forms import FincaForm, ZonaForm
from security.decorators import role_required

@login_required(login_url='/login/')
def finca_list(request):
    """Vista para listar fincas según el usuario autenticado"""
    search_query = request.GET.get('search', '')
    estado_filter = request.GET.get('estado', '')
    
    # Filtrar fincas según el rol del usuario
    if request.user.is_admin():
        fincas = Finca.objects.all()
    else:
        # Obtener fincas donde es propietario o está asignado
        fincas = Finca.objects.filter(
            Q(propietario=request.user) | Q(usuarios_asignados=request.user)
        ).distinct()
    
    if search_query:
        fincas = fincas.filter(
            Q(nombre__icontains=search_query) | 
            Q(ubicacion__icontains=search_query) | 
            Q(cultivo_actual__icontains=search_query)
        )
    
    if estado_filter:
        fincas = fincas.filter(estado=estado_filter)
    
    paginator = Paginator(fincas, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'estado_filter': estado_filter,
        'estado_choices': Finca.ESTADO_CHOICES,
    }
    return render(request, 'farms/finca_list.html', context)

@role_required('ADMIN', 'AGRONOMO', 'TECNICO')
def finca_create(request):
    """Vista para crear una nueva finca"""
    if request.method == 'POST':
        form = FincaForm(request.POST)
        if form.is_valid():
            finca = form.save(commit=False)
            finca.propietario = request.user
            finca.save()
            form.save_m2m()  # Guardar relaciones ManyToMany
            messages.success(request, f'Finca "{finca.nombre}" creada exitosamente.')
            return redirect('finca_detail', finca_id=finca.id)
    else:
        form = FincaForm()
    
    return render(request, 'farms/finca_form.html', {
        'form': form,
        'title': 'Crear Nueva Finca',
        'button_text': 'Crear Finca'
    })

@login_required(login_url='/login/')
def finca_detail(request, finca_id):
    """Vista para ver detalle de una finca"""
    finca = get_object_or_404(Finca, id=finca_id)
    
    # Verificar acceso
    if not finca.tiene_acceso(request.user):
        messages.error(request, 'No tienes permisos para ver esta finca.')
        return redirect('finca_list')
    
    # Obtener zonas de la finca
    zonas = finca.zonas.all()
    
    context = {
        'finca': finca,
        'zonas': zonas,
    }
    return render(request, 'farms/finca_detail.html', context)

@login_required(login_url='/login/')
def finca_edit(request, finca_id):
    """Vista para editar una finca"""
    finca = get_object_or_404(Finca, id=finca_id)
    
    # Verificar permisos: solo propietario o admin pueden editar
    if not (request.user.is_admin() or request.user == finca.propietario):
        messages.error(request, 'No tienes permisos para editar esta finca.')
        return redirect('finca_detail', finca_id=finca.id)
    
    if request.method == 'POST':
        form = FincaForm(request.POST, instance=finca)
        if form.is_valid():
            form.save()
            messages.success(request, f'Finca "{finca.nombre}" actualizada exitosamente.')
            return redirect('finca_detail', finca_id=finca.id)
    else:
        form = FincaForm(instance=finca)
    
    return render(request, 'farms/finca_form.html', {
        'form': form,
        'finca': finca,
        'title': 'Editar Finca',
        'button_text': 'Guardar Cambios'
    })

@role_required('ADMIN')
def finca_delete(request, finca_id):
    """Vista para eliminar una finca (solo administradores)"""
    finca = get_object_or_404(Finca, id=finca_id)
    
    if request.method == 'POST':
        nombre = finca.nombre
        finca.delete()
        messages.success(request, f'Finca "{nombre}" eliminada exitosamente.')
        return redirect('finca_list')
    
    return render(request, 'farms/finca_confirm_delete.html', {'finca': finca})

# Vista legacy para compatibilidad
@login_required(login_url='/login/')
def finca(request):
    """Redirección a la nueva vista de listado"""
    return redirect('finca_list')

# ============ VISTAS DE ZONAS ============

@role_required('ADMIN', 'AGRONOMO', 'TECNICO')
def zona_create(request, finca_id):
    """Vista para crear una nueva zona en una finca"""
    finca = get_object_or_404(Finca, id=finca_id)
    
    # Verificar acceso
    if not (request.user.is_admin() or request.user == finca.propietario):
        messages.error(request, 'No tienes permisos para crear zonas en esta finca.')
        return redirect('finca_detail', finca_id=finca.id)
    
    if request.method == 'POST':
        form = ZonaForm(request.POST)
        if form.is_valid():
            zona = form.save(commit=False)
            zona.finca = finca
            zona.save()
            messages.success(request, f'Zona "{zona.nombre}" creada exitosamente.')
            return redirect('finca_detail', finca_id=finca.id)
    else:
        form = ZonaForm()
    
    return render(request, 'farms/zona_form.html', {
        'form': form,
        'finca': finca,
        'title': 'Crear Nueva Zona',
        'button_text': 'Crear Zona'
    })

@login_required(login_url='/login/')
def zona_edit(request, zona_id):
    """Vista para editar una zona"""
    zona = get_object_or_404(Zona, id=zona_id)
    
    # Verificar permisos
    if not (request.user.is_admin() or request.user == zona.finca.propietario):
        messages.error(request, 'No tienes permisos para editar esta zona.')
        return redirect('finca_detail', finca_id=zona.finca.id)
    
    if request.method == 'POST':
        form = ZonaForm(request.POST, instance=zona)
        if form.is_valid():
            form.save()
            messages.success(request, f'Zona "{zona.nombre}" actualizada exitosamente.')
            return redirect('finca_detail', finca_id=zona.finca.id)
    else:
        form = ZonaForm(instance=zona)
    
    return render(request, 'farms/zona_form.html', {
        'form': form,
        'finca': zona.finca,
        'zona': zona,
        'title': 'Editar Zona',
        'button_text': 'Guardar Cambios'
    })

@role_required('ADMIN', 'AGRONOMO')
def zona_delete(request, zona_id):
    """Vista para eliminar una zona"""
    zona = get_object_or_404(Zona, id=zona_id)
    finca_id = zona.finca.id
    
    # Verificar permisos
    if not (request.user.is_admin() or request.user == zona.finca.propietario):
        messages.error(request, 'No tienes permisos para eliminar esta zona.')
        return redirect('finca_detail', finca_id=finca_id)
    
    if request.method == 'POST':
        nombre = zona.nombre
        zona.delete()
        messages.success(request, f'Zona "{nombre}" eliminada exitosamente.')
        return redirect('finca_detail', finca_id=finca_id)
    
    return render(request, 'farms/zona_confirm_delete.html', {'zona': zona})
