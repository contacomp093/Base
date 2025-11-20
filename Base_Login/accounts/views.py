# accounts/views.py (importar lo necesario)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from .forms import ProviderApplicationForm
from .models import ProviderApplication

import uuid

# 1) Formulario público de solicitud
def affiliate_apply(request):
    if request.method == "POST":
        form = ProviderApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.save()

            # Preparar URL de registro (token)
            token = application.token
            register_path = reverse("accounts:provider_register", args=[str(token)])
            register_url = request.build_absolute_uri(register_path)

            # Enviar email premium al solicitante (HTML) y copia a admin de pruebas
            send_provider_application_emails(application, register_url)

            return redirect("accounts:affiliate_thanks")
    else:
        form = ProviderApplicationForm()
    return render(request, "accounts/affiliate_apply.html", {"form": form})

# 2) Página de gracias (simple)
def affiliate_thanks(request):
    return render(request, "accounts/affiliate_thanks.html")

# Helper para enviar emails
def send_provider_application_emails(application: ProviderApplication, register_url: str):
    subject = "Solicitud recibida — Afiliación a MyPanel"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [application.contact_email]
    # copia a pruebas
    cc = [ "contacomp093@gmail.com" ]  # correo de pruebas

    # HTML para el proveedor (premium)
    html_content = render_to_string("accounts/emails/provider_application_email.html", {
        "application": application,
        "register_url": register_url,
        "company_name": getattr(settings, "PROJECT_NAME", "Mi Plataforma"),
    })

    text_content = render_to_string("accounts/emails/provider_application_email.txt", {
        "application": application,
        "register_url": register_url,
        "company_name": getattr(settings, "PROJECT_NAME", "Mi Plataforma"),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email, cc=cc)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

# 3) Registro real del proveedor (token links)
from django import forms
from django.contrib.auth.forms import UserCreationForm

class ProviderRegistrationForm(UserCreationForm):
    # campos para la tienda
    store_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"input-field"}))
    store_address = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"input-field"}))
    store_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"input-field"}))
    store_service_type = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"input-field"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

def provider_register(request, token):
    # buscar la solicitud
    application = get_object_or_404(ProviderApplication, token=token)

    # solo permitir si está pendiente o aprobado (pero no registrado)
    if application.status not in ("pending", "approved"):
        messages.error(request, "Este link ya no es válido o ya fue usado.")
        return redirect("accounts:affiliate_thanks")

    if request.method == "POST":
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            # crear UserProfile con role='provider' (ajusta a tu modelo)
            profile = UserProfile.objects.create(
                user=user,
                role="provider",
                store_name=form.cleaned_data.get("store_name"),
                store_address=form.cleaned_data.get("store_address"),
                store_phone=form.cleaned_data.get("store_phone"),
                store_service_type=form.cleaned_data.get("store_service_type"),
            )

            # marcar la aplicación como registrada
            application.mark_registered()

            # opcional: iniciar sesión automáticamente
            login(request, user)

            messages.success(request, "Cuenta de proveedor creada correctamente.")
            return redirect("dashboard:index")  # ajusta al nombre de tu dashboard
    else:
        form = ProviderRegistrationForm(initial={
            "email": application.contact_email,
            "store_name": application.store_name or "",
        })

    return render(request, "accounts/provider_register.html", {
        "form": form,
        "application": application,
    })
