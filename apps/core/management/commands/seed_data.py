"""
Comando para cargar datos iniciales (seed) en la base de datos.
Uso: python manage.py seed_data
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
import os


class Command(BaseCommand):
    help = 'Carga datos iniciales desde fixtures. Uso: python manage.py seed_data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fixtures-dir',
            type=str,
            default='fixtures',
            help='Directorio donde están los fixtures (default: fixtures)',
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='No fallar si los datos ya existen',
        )

    def handle(self, *args, **options):
        fixtures_dir = options.get('fixtures_dir', 'fixtures')
        skip_existing = options.get('skip_existing', False)

        fixtures_path = Path(fixtures_dir)

        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Cargando datos iniciales (seed)'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')

        if not fixtures_path.exists():
            self.stdout.write(self.style.WARNING(f'⚠ El directorio {fixtures_dir} no existe.'))
            self.stdout.write(self.style.WARNING('No hay datos para cargar.'))
            return

        # Buscar archivos de fixtures
        fixture_files = sorted(fixtures_path.glob('*_data.json'))

        if not fixture_files:
            self.stdout.write(self.style.WARNING(f'⚠ No se encontraron archivos de fixtures en {fixtures_dir}'))
            self.stdout.write(self.style.WARNING('Crea fixtures primero con: python manage.py export_data'))
            return

        loaded_count = 0
        error_count = 0

        for fixture_file in fixture_files:
            try:
                self.stdout.write(f'Cargando {fixture_file.name}...')
                call_command('loaddata', str(fixture_file), verbosity=1)
                self.stdout.write(self.style.SUCCESS(f'✓ {fixture_file.name} cargado exitosamente'))
                loaded_count += 1
            except Exception as e:
                if skip_existing and 'already exists' in str(e).lower():
                    self.stdout.write(self.style.WARNING(f'⚠ {fixture_file.name} ya existe, omitiendo...'))
                else:
                    self.stdout.write(self.style.ERROR(f'✗ Error cargando {fixture_file.name}: {str(e)}'))
                    error_count += 1
                    if not skip_existing:
                        raise CommandError(f'Error cargando {fixture_file.name}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        if error_count == 0:
            self.stdout.write(self.style.SUCCESS(f'✓ {loaded_count} archivo(s) cargado(s) exitosamente!'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ {loaded_count} cargado(s), {error_count} error(es)'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
