from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nombres',
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apellidos',
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Correo Electrónico',
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Teléfono',
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Contraseña',
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar Contraseña',
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
    }))
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                   'phone', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
     username = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Correo Electrónico',
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
        'type': 'email',
    }))
     password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Contraseña',
        'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
        'type': 'password',
    }))

class UserEditForm(UserChangeForm):
    """Formulario para editar usuarios existentes (para administradores)"""
    password = None  # Ocultar el campo de contraseña en el formulario de edición
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'role', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'placeholder': 'Nombres'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'placeholder': 'Apellidos'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'placeholder': 'Correo Electrónico'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'placeholder': 'Teléfono'
            }),
            'role': forms.Select(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-primary'
            }),
        }

class UserCreateForm(UserCreationForm):
    """Formulario para crear nuevos usuarios (para administradores)"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'role', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Nombres'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Apellidos'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Correo Electrónico'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Teléfono'
            }),
            'role': forms.Select(attrs={
                'class': 'form-select w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
            'placeholder': 'Confirmar Contraseña'
        })