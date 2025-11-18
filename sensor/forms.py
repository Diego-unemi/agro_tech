from django import forms
from .models import Sensor
from farms.models import Finca, Zona

class SensorForm(forms.ModelForm):
    # Campo para seleccionar finca primero (para filtrar zonas)
    finca = forms.ModelChoiceField(
        queryset=Finca.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
            'onchange': 'this.form.submit()'  # Para actualizar las zonas disponibles
        }),
        label='Finca (opcional)'
    )
    
    class Meta:
        model = Sensor
        fields = ['nombre', 'codigo_serial', 'tipo', 'zona', 'estado', 'fecha_instalacion', 
                  'fabricante', 'modelo', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'placeholder': 'Nombre identificativo del sensor'
            }),
            'codigo_serial': forms.TextInput(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'placeholder': 'Código serial único'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
            }),
            'zona': forms.Select(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal'
            }),
            'fecha_instalacion': forms.DateInput(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'type': 'date'
            }),
            'fabricante': forms.TextInput(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'placeholder': 'Fabricante del sensor'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'placeholder': 'Modelo del sensor'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-r-lg text-text-dark dark:text-text-light focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 h-14 placeholder:text-zinc-400 dark:placeholder-zinc-500 p-3.5 text-base font-normal',
                'placeholder': 'Descripción adicional',
                'rows': 3
            }),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar fincas según el usuario
        if user:
            if not user.is_admin():
                from django.db.models import Q
                self.fields['finca'].queryset = Finca.objects.filter(
                    Q(propietario=user) | Q(usuarios_asignados=user)
                ).distinct()
        
        # Si hay una finca seleccionada, filtrar zonas
        if 'finca' in self.data:
            try:
                finca_id = int(self.data.get('finca'))
                self.fields['zona'].queryset = self.fields['zona'].queryset.filter(finca_id=finca_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.zona:
            # Si estamos editando, mostrar zonas de la finca actual
            self.fields['zona'].queryset = self.fields['zona'].queryset.filter(finca=self.instance.zona.finca)
            self.fields['finca'].initial = self.instance.zona.finca

