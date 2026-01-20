"""
Comando personalizado de Django que ejecuta makemigrations + migrate automáticamente.
Uso: python manage.py migrate_auto [app_name]
Si no se especifica app_name, ejecuta para todas las apps.
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Ejecuta makemigrations y luego migrate automáticamente. Uso: python manage.py migrate_auto [app_name]'

    def add_arguments(self, parser):
        parser.add_argument(
            'app_name',
            nargs='?',
            type=str,
            help='Nombre de la app a migrar (opcional). Si no se especifica, migra todas las apps.',
        )

    def handle(self, *args, **options):
        app_name = options.get('app_name', None)

        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Creando y ejecutando migraciones de Django'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')

        # Paso 1: Crear migraciones
        self.stdout.write(self.style.WARNING('Paso 1: Creando archivos de migración...'))
        self.stdout.write('')

        try:
            if app_name:
                call_command('makemigrations', app_name, verbosity=1)
            else:
                call_command('makemigrations', verbosity=1)
        except CommandError as e:
            self.stdout.write(self.style.ERROR('=' * 50))
            self.stdout.write(self.style.ERROR('ERROR: No se pudieron crear las migraciones'))
            self.stdout.write(self.style.ERROR(str(e)))
            self.stdout.write(self.style.ERROR('=' * 50))
            raise

        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Paso 2: Aplicando migraciones a la base de datos...'))
        self.stdout.write('')

        # Paso 2: Aplicar migraciones (usar el comando original de Django)
        try:
            # Usar call_command con el comando original de Django
            if app_name:
                call_command('migrate', app_name, verbosity=1)
            else:
                call_command('migrate', verbosity=1)
        except CommandError as e:
            self.stdout.write(self.style.ERROR('=' * 50))
            self.stdout.write(self.style.ERROR('ERROR: Las migraciones fallaron'))
            self.stdout.write(self.style.ERROR(str(e)))
            self.stdout.write(self.style.ERROR('=' * 50))
            raise

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Migraciones creadas y aplicadas exitosamente!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
