from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    # Login
    path('login/', 
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 🔐 Reset password (vista principal)
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'
         ),
         name='password_reset'),

    # 🔐 Mensaje enviado
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    # 🔐 Confirmación con token
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    # 🔐 Proceso finalizado
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),


    # NUEVAS RUTAS afiliación / proveedores
    path('affiliate/apply/', views.affiliate_apply, name='affiliate_apply'),
    path('affiliate/thanks/', views.affiliate_thanks, name='affiliate_thanks'),
    path('provider/register/<uuid:token>/', views.provider_register, name='provider_register'),
]
