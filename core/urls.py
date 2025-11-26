from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('buscaHogar/', views.buscaHogar, name='buscaHogar'),
     path('lista_mascotas/', views.lista_mascotas, name='lista_mascotas'),
]
