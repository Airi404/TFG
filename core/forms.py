# core/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Mascota

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "class": "w-full px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-orange-400 focus:outline-none transition"
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado")
        return email
    
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