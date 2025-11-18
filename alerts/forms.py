from django import forms
from .models import UmbralAlerta

class UmbralAlertaForm(forms.ModelForm):
    class Meta:
        model = UmbralAlerta
        fields = [
            'zona',
            'parametro',
            'valor_minimo',
            'valor_maximo',
            'nivel_severidad',
            'activo'
        ]
        widgets = {
            'zona': forms.Select(attrs={
                'class': 'form-select w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary'
            }),
            'parametro': forms.Select(attrs={
                'class': 'form-select w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary'
            }),
            'valor_minimo': forms.NumberInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'step': '0.1'
            }),
            'valor_maximo': forms.NumberInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'step': '0.1'
            }),
            'nivel_severidad': forms.Select(attrs={
                'class': 'form-select w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-primary border-gray-300 rounded focus:ring-2 focus:ring-primary'
            })
        }

