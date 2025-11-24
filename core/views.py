from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .forms import MascotaForm
from django.contrib import messages
from transformers import AutoTokenizer, AutoModelForMultipleChoice
import torch
import re

tokenizer = AutoTokenizer.from_pretrained("prajjwal1/roberta_hellaswag")
model = AutoModelForMultipleChoice.from_pretrained("prajjwal1/roberta_hellaswag")


def home(request):
    return render(request, 'core/home.html')

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Loguea al usuario automáticamente
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "registration/signup.html", {"form": form})

def analizar_texto_commonsense(texto):
    if not texto.strip():
        return False, "Descripción vacía."

    # Extraer descripción
    match = re.search(r"Descripción:\s*(.*)", texto)
    descripcion = match.group(1) if match else texto

    # Construir opciones
    opciones = [
        f"{descripcion} Esto es realista.",
        f"{descripcion} Esto es absurdo."
    ]

    # Tokenizar como multiple choice
    inputs = tokenizer([descripcion, descripcion], opciones, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits

    pred = torch.argmax(logits, dim=1).item()

    if pred == 0:
        return True, "Contenido coherente."
    else:
        return False, "Contenido incoherente o absurdo."


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
            permitido, mensaje = analizar_texto_huggingface(contenido)

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
