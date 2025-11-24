from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .forms import MascotaForm
from django.contrib import messages
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re

tokenizer = AutoTokenizer.from_pretrained("roberta-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")


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

def analizar_texto_huggingface(texto):
    """
    Analiza coherencia combinando reglas simples + Roberta-MNLI.
    Devuelve True si es coherente, False si parece incoherente o absurdo.
    """
    # Reglas simples: descartar solo nombres raros o textos vacíos
    if not texto.strip():
        return False, "Descripción vacía."

    # Ignorar nombres demasiado cortos
    if len(texto.split("\n")[0].split(":")[-1].strip()) < 2:
        return True, "Contenido permitido."

    # Extraer solo la descripción para MNLI
    match = re.search(r"Descripción:\s*(.*)", texto)
    descripcion = match.group(1) if match else texto

    # MNLI solo en la descripción
    hypothesis = "This is a valid pet description."
    inputs = tokenizer(descripcion, hypothesis, return_tensors='pt', truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    probabilities = torch.softmax(logits, dim=1)
    labels = ["contradiction", "neutral", "entailment"]
    pred_label = labels[probabilities.argmax()]

    if pred_label == "entailment" or len(descripcion) < 20:
        # Si MNLI dice entailment o la descripción es corta y normal, aceptamos
        return True, "Contenido coherente."
    else:
        return False, "Contenido incoherente o sospechoso."


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
