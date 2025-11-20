from django.contrib import admin
from .models import ProviderApplication

@admin.register(ProviderApplication)
class ProviderApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "store_name",
        "contact_email",
        "created_at",
        "is_used",
    )

    list_filter = ("is_used", "created_at")

    search_fields = ("store_name", "contact_name", "contact_email")
