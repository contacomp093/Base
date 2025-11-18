from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from core.views import dashboard

# Ruta para permitir cambiar idioma via URL y cookies
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Rutas que soportan idiomas (i18n)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

    # Dashboard protegido
    path('dashboard/', dashboard, name='dashboard'),

    # Redirección raíz → login
    path('', RedirectView.as_view(url='/accounts/login/')),
)
