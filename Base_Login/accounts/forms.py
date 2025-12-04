from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProviderApplication


# ========================================================
# FORM 1 - Formulario de solicitud (affiliate_apply)
# ========================================================
class ProviderApplicationForm(forms.ModelForm):
    class Meta:
        model = ProviderApplication
        fields = [
            'contact_name',
            'contact_email',
            'contact_phone',
            'city',
            'store_name',
            'message',
        ]

        labels = {
            'contact_name': _("Nombre completo"),
            'contact_email': _("Correo electrónico"),
            'contact_phone': _("Teléfono"),
            'city': _("Ciudad"),
            'store_name': _("Nombre de la tienda"),
            'message': _("Mensaje (opcional)"),
        }

        widgets = {
            'contact_name': forms.TextInput(attrs={'class': 'input-primary'}),
            'contact_email': forms.EmailInput(attrs={'class': 'input-primary'}),
            'contact_phone': forms.TextInput(attrs={'class': 'input-primary'}),
            'city': forms.TextInput(attrs={'class': 'input-primary'}),
            'store_name': forms.TextInput(attrs={'class': 'input-primary'}),
            'message': forms.Textarea(attrs={'class': 'textarea-primary'}),
        }


# ========================================================
# FORM 2 - Formulario para registro final del proveedor
# ========================================================
class ProviderRegistrationForm(UserCreationForm):

    store_name = forms.CharField(
        required=True,
        label="Nombre de la tienda",
        widget=forms.TextInput(attrs={"class": "input-primary w-full"})
    )

    store_address = forms.CharField(
        required=False,
        label="Dirección",
        widget=forms.TextInput(attrs={"class": "input-primary w-full"})
    )

    store_phone = forms.CharField(
        required=False,
        label="Teléfono de la tienda",
        widget=forms.TextInput(attrs={"class": "input-primary w-full"})
    )

    store_service_type = forms.CharField(
        required=False,
        label="Tipo de servicio",
        widget=forms.TextInput(attrs={"class": "input-primary w-full"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
