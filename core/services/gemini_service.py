import google.generativeai as genai
from django.conf import settings

# Configurar API
genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def preguntar_a_gemini(mensaje):
    respuesta = model.generate_content(mensaje)
    return respuesta.text
