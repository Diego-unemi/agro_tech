from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserEditForm, UserCreateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .decorators import admin_required
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'security/registro.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'security/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def success(request):
    return render(request, 'security/success.html')

@admin_required
def user_list(request):
    """Vista para listar todos los usuarios (solo administradores)"""
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    
    users = CustomUser.objects.all()
    
    if search_query:
        users = users.filter(
            first_name__icontains=search_query
        ) | users.filter(
            last_name__icontains=search_query
        ) | users.filter(
            email__icontains=search_query
        )
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'role_choices': CustomUser.ROLE_CHOICES,
    }
    return render(request, 'security/user_list.html', context)

@admin_required
def user_create(request):
    """Vista para crear un nuevo usuario (solo administradores)"""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.get_full_name()} creado exitosamente.')
            return redirect('user_list')
    else:
        form = UserCreateForm()
    
    return render(request, 'security/user_form.html', {
        'form': form,
        'title': 'Crear Usuario',
        'button_text': 'Crear Usuario'
    })

@admin_required
def user_edit(request, user_id):
    """Vista para editar un usuario existente (solo administradores)"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {user.get_full_name()} actualizado exitosamente.')
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'security/user_form.html', {
        'form': form,
        'user_obj': user,
        'title': 'Editar Usuario',
        'button_text': 'Guardar Cambios'
    })

@admin_required
def user_delete(request, user_id):
    """Vista para eliminar un usuario (solo administradores)"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.user.id == user.id:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('user_list')
    
    if request.method == 'POST':
        user_name = user.get_full_name()
        user.delete()
        messages.success(request, f'Usuario {user_name} eliminado exitosamente.')
        return redirect('user_list')
    
    return render(request, 'security/user_confirm_delete.html', {'user_obj': user})

@login_required
def user_profile(request):
    """Vista para ver y editar el perfil del usuario autenticado"""
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        form.fields['role'].disabled = True  # No permitir cambiar el propio rol
        form.fields['is_active'].disabled = True  # No permitir desactivarse
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('user_profile')
    else:
        form = UserEditForm(instance=request.user)
        form.fields['role'].disabled = True
        form.fields['is_active'].disabled = True
    
    return render(request, 'security/user_profile.html', {'form': form})
