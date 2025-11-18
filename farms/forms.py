from django import forms
from .models import Finca, Zona

class FincaForm(forms.ModelForm):
    class Meta:
        model = Finca
        fields = ['nombre', 'ubicacion', 'direccion', 'area_total', 'cultivo_actual', 
                  'usuarios_asignados', 'estado', 'notas']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Nombre de la finca'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Ciudad, provincia o coordenadas'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Dirección completa',
                'rows': 3
            }),
            'area_total': forms.NumberInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Área en hectáreas',
                'step': '0.01'
            }),
            'cultivo_actual': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Tipo de cultivo'
            }),
            'usuarios_asignados': forms.SelectMultiple(attrs={
                'class': 'form-select w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'size': '5'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Notas adicionales',
                'rows': 4
            }),
        }

class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ['nombre', 'tipo_cultivo', 'area', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Nombre de la zona'
            }),
            'tipo_cultivo': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Tipo de cultivo'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Área en hectáreas',
                'step': '0.01'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary',
                'placeholder': 'Descripción de la zona',
                'rows': 3
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary'
            }),
        }

