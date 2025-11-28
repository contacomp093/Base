# Base_Login/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from accounts.views import email_diagnostic


urlpatterns = [
    # Necesario para cambiar idioma vía URL o cookies
    path('i18n/', include('django.conf.urls.i18n')),

    # Ruta técnica para pruebas de email (SIN idioma)
    path("diagnostic/email/", email_diagnostic),
]

# Rutas traducibles
urlpatterns += i18n_patterns(

    # Admin
    path('admin/', admin.site.urls),

    # Accounts
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # Dashboard (NUEVA APP)
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),

    # Redirige a login
    path('', RedirectView.as_view(url='/accounts/login/')),
    
    
)