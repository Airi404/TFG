# core/forms.py
from django import forms
from .models import Mascota
    
class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'descripcion', 'raza', 'tipo', 'años', 'caracter', 'foto']
        widgets = {
                    'nombre': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
                    'descripcion': forms.Textarea(attrs={'class': 'w-full border rounded-lg px-3 py-2', 'rows': 4}),
                    'raza': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
                    'tipo': forms.Select(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
                    'años': forms.NumberInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
                    'caracter': forms.Select(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
                    'foto': forms.FileInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
                }