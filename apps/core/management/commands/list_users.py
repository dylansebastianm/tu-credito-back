"""
Comando para listar usuarios en la base de datos.
Útil para verificar usuarios en producción.
Uso: python manage.py list_users
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Lista todos los usuarios en la base de datos con sus detalles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Filtrar por username específico',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Filtrar por email específico',
        )
        parser.add_argument(
            '--superusers-only',
            action='store_true',
            help='Mostrar solo superusuarios',
        )

    def handle(self, *args, **options):
        users = User.objects.all()

        # Aplicar filtros
        if options['username']:
            users = users.filter(username=options['username'])
        
        if options['email']:
            users = users.filter(email=options['email'])
        
        if options['superusers_only']:
            users = users.filter(is_superuser=True)

        total = users.count()

        if total == 0:
            self.stdout.write(self.style.WARNING('⚠ No se encontraron usuarios en la base de datos.'))
            self.stdout.write(self.style.WARNING('⚠ Puedes crear un superusuario con:'))
            self.stdout.write(self.style.WARNING('   python manage.py create_superuser_if_not_exists --username admin --email admin@example.com --password tu_password'))
            return

        self.stdout.write(self.style.SUCCESS(f'\n✓ Total de usuarios encontrados: {total}\n'))
        self.stdout.write('=' * 80)

        for user in users:
            self.stdout.write(f'\n📋 Usuario: {user.username}')
            self.stdout.write(f'   ID: {user.id}')
            self.stdout.write(f'   Email: {user.email or "(sin email)"}')
            self.stdout.write(f'   Nombre completo: {user.get_full_name() or "(sin nombre)"}')
            self.stdout.write(f'   Activo: {"✓ Sí" if user.is_active else "✗ No"}')
            self.stdout.write(f'   Staff: {"✓ Sí" if user.is_staff else "✗ No"}')
            self.stdout.write(f'   Superusuario: {"✓ Sí" if user.is_superuser else "✗ No"}')
            self.stdout.write(f'   Último login: {user.last_login or "(nunca)"}')
            self.stdout.write(f'   Fecha de registro: {user.date_joined}')
            self.stdout.write('-' * 80)

        self.stdout.write('\n')
