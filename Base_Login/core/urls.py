# Base_Login/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    # Necesario para cambiar idioma vía URL o cookies
    path('i18n/', include('django.conf.urls.i18n')),
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