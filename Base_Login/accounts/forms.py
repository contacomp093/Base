from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ProviderApplication

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

        # 🔥 Labels traducibles (NO texto duro en español)
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

