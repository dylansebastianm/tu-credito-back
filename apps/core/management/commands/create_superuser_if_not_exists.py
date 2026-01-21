"""
Comando para crear un superusuario si no existe.
Útil para producción donde no se puede usar Shell interactivo.
Uso: python manage.py create_superuser_if_not_exists
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea un superusuario si no existe. Usa variables de entorno: SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username del superusuario (o usar variable de entorno SUPERUSER_USERNAME)',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email del superusuario (o usar variable de entorno SUPERUSER_EMAIL)',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password del superusuario (o usar variable de entorno SUPERUSER_PASSWORD)',
        )

    def handle(self, *args, **options):
        username = options.get('username') or os.environ.get('SUPERUSER_USERNAME')
        email = options.get('email') or os.environ.get('SUPERUSER_EMAIL', '')
        password = options.get('password') or os.environ.get('SUPERUSER_PASSWORD')

        if not username:
            self.stdout.write(self.style.WARNING('⚠ No se proporcionó username. Usa --username o variable SUPERUSER_USERNAME'))
            self.stdout.write(self.style.WARNING('⚠ Saltando creación de superusuario...'))
            return

        if not password:
            self.stdout.write(self.style.WARNING('⚠ No se proporcionó password. Usa --password o variable SUPERUSER_PASSWORD'))
            self.stdout.write(self.style.WARNING('⚠ Saltando creación de superusuario...'))
            return

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.is_superuser:
                self.stdout.write(self.style.SUCCESS(f'✓ El superusuario "{username}" ya existe.'))
            else:
                # Si existe pero no es superusuario, hacerlo superusuario
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ El usuario "{username}" ahora es superusuario.'))
            return

        # Crear superusuario
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Superusuario "{username}" creado exitosamente!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creando superusuario: {str(e)}'))
            # No hacer raise para que el build no falle si hay error
            return
