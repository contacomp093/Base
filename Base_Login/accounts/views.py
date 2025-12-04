# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import User

from .models import ProviderApplication, UserProfile
from .forms import ProviderApplicationForm, ProviderRegistrationForm


# ===========================================================
# 1. FORMULARIO DE SOLICITUD (affiliate_apply)
# ===========================================================
def affiliate_apply(request):
    if request.method == "POST":
        form = ProviderApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()

            token = application.token
            register_path = reverse("accounts:provider_register", args=[str(token)])
            register_url = f"{settings.DEFAULT_DOMAIN}{register_path}"

            # Enviar email (ya lo tienes implementado)
            from .views import send_provider_application_emails
            send_provider_application_emails(application, register_url)

            return redirect("accounts:affiliate_thanks")

    else:
        form = ProviderApplicationForm()

    return render(request, "accounts/affiliate_apply.html", {"form": form})


def affiliate_thanks(request):
    return render(request, "accounts/affiliate_thanks.html")

# ===========================================================
# HELPER PARA ENVIAR EMAILS DE AFILIACIÓN
# ===========================================================
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from threading import Thread

def send_provider_application_emails(application, register_url):
    """
    Envía el correo premium al usuario que hizo la solicitud para completar
    el registro del proveedor. Se envía en un hilo separado para evitar bloqueos.
    """

    def _send():
        subject = "Solicitud recibida — Afiliación a MyPanel"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [application.contact_email]

        # Copia para pruebas
        cc = ["contacomp093@gmail.com"]

        # Render HTML
        html_content = render_to_string("accounts/emails/provider_application_email.html", {
            "application": application,
            "register_url": register_url,
            "company_name": getattr(settings, "PROJECT_NAME", "Mi Plataforma"),
        })

        # Render versión texto
        text_content = render_to_string("accounts/emails/provider_application_email.txt", {
            "application": application,
            "register_url": register_url,
            "company_name": getattr(settings, "PROJECT_NAME", "Mi Plataforma"),
        })

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email, cc=cc)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

    Thread(target=_send).start()

# ===========================================================
# 2. REGISTRO REAL DEL PROVEEDOR DESDE EL LINK DEL EMAIL
# ===========================================================
def provider_register(request, token):

    # 1. Obtener la solicitud por token
    application = get_object_or_404(ProviderApplication, token=token)

    # 2. Validar estado
    if application.status not in ("pending", "approved"):
        messages.error(request, "Este enlace ya fue usado o no es válido.")
        return redirect("accounts:affiliate_thanks")

    # 3. PROCESAR FORMULARIO
    if request.method == "POST":
        form = ProviderRegistrationForm(request.POST)

        if form.is_valid():

            # 4. Crear el usuario real (del sistema)
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            # 5. Completar el UserProfile
            profile = user.userprofile
            profile.role = "provider"
            profile.store_name = form.cleaned_data["store_name"]
            profile.store_address = form.cleaned_data["store_address"]
            profile.store_phone = form.cleaned_data["store_phone"]
            profile.store_service_type = form.cleaned_data["store_service_type"]
            profile.save()

            # 6. Marcar la solicitud como registrada
            application.mark_registered()

            # 7. Login automático
            login(request, user)

            # 8. Redirigir al dashboard
            messages.success(request, "Cuenta de proveedor creada correctamente.")
            return redirect("dashboard:index")

    # 9. Mostrar formulario (GET)
    else:
        form = ProviderRegistrationForm(initial={
            "email": application.contact_email,
            "store_name": application.store_name or "",
        })

    return render(request, "accounts/provider_register.html", {
        "form": form,
        "application": application,
    })
