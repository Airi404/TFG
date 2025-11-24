from django.urls import path
from . import views
from .views import signup_view
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name='home'),
    path("signup/", signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/",auth_views.LogoutView.as_view(next_page='home'),
            name="logout"
        ),      
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="registration/reset_form.html"), 
         name="password_reset"),

    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/reset_done.html"), 
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/reset_confirm.html"), 
         name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/reset_complete.html"), 
         name="password_reset_complete"),

     path('buscaHogar/', views.buscaHogar, name='buscaHogar'),
     path('lista_mascotas/', views.lista_mascotas, name='lista_mascotas'),

]
