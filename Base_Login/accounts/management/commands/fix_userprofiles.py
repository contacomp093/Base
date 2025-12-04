from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = "Crea UserProfile para usuarios que aún no lo tienen."

    def handle(self, *args, **kwargs):
        created_count = 0

        users = User.objects.all()

        for user in users:
            # Si el usuario NO tiene UserProfile → crearlo
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(
                    user=user,
                    role="client"  # Rol por defecto
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Perfiles creados: {created_count}."
        ))

        if created_count == 0:
            self.stdout.write("Todos los usuarios ya tenían perfil.")
