import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone


class ProviderApplication(models.Model):
    # -----------------------------
    # Datos de contacto del solicitante
    # -----------------------------
    contact_name = models.CharField(max_length=150)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=50)

    # -----------------------------
    # Datos de la tienda / servicio
    # -----------------------------
    store_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(blank=True)

    # -----------------------------
    # Estado del proceso
    # -----------------------------
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # -----------------------------
    # Token y control del enlace mágico
    # -----------------------------
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Muy importante: usar función para default en vez de ejecutar la operación directo
    def default_expiry():
        return timezone.now() + timedelta(days=7)

    expires_at = models.DateTimeField(default=default_expiry)
    is_used = models.BooleanField(default=False)

    # -----------------------------
    # Métodos
    # -----------------------------
    def is_valid(self):
        return timezone.now() < self.expires_at and not self.is_used

    def __str__(self):
        return f"{self.store_name} ({self.contact_email})"
