from django.shortcuts import render
from django.shortcuts import redirect
from .forms import MascotaForm
from django.contrib import messages
from transformers import AutoTokenizer, AutoModelForMultipleChoice
import torch
import re

tokenizer = AutoTokenizer.from_pretrained("prajjwal1/roberta_hellaswag")
model = AutoModelForMultipleChoice.from_pretrained("prajjwal1/roberta_hellaswag")


def home(request):
    return render(request, 'core/home.html')

from django.http import JsonResponse
from .services.gemini_service import preguntar_a_gemini

def analizar_texto_commonsense(request):
    pregunta = request.GET.get("q", "Hola, ¿qué puedes hacer?")
    respuesta = preguntar_a_gemini(pregunta)

    return JsonResponse({
        "pregunta": pregunta,
        "respuesta": respuesta
    })


def buscaHogar(request):
    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            # Concatenar todos los campos importantes del formulario
            contenido = (
                f"Nombre: {form.cleaned_data['nombre']}\n"
                f"Descripción: {form.cleaned_data['descripcion']}\n"
                f"Raza: {form.cleaned_data['raza']}\n"
                f"Tipo: {form.cleaned_data['tipo']}\n"
                f"Carácter: {form.cleaned_data['caracter']}"
            )

            # Analizar coherencia del texto
            permitido, mensaje = analizar_texto_commonsense(contenido)

            if not permitido:
                messages.error(request, mensaje)
                return redirect('buscaHogar')

            # Guardar mascota si pasa la moderación
            form.save()
            messages.success(request, "Mascota registrada correctamente.")
            return redirect('buscaHogar')
    else:
        form = MascotaForm()

    return render(request, 'core/buscaHogar.html', {'form': form})

from django.shortcuts import render
from .models import Mascota  # Importa tu modelo

def lista_mascotas(request):
    # Consulta todas las mascotas de la base de datos
    mascotas = Mascota.objects.all()
    return render(request, 'core/lista_mascotas.html', {'mascotas': mascotas})
