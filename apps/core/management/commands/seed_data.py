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
        all_fixture_files = list(fixtures_path.glob('*_data.json'))

        if not all_fixture_files:
            self.stdout.write(self.style.WARNING(f'⚠ No se encontraron archivos de fixtures en {fixtures_dir}'))
            self.stdout.write(self.style.WARNING('Crea fixtures primero con: python manage.py export_data'))
            return

        # Orden de carga: primero bancos, luego clientes, luego créditos, luego usuarios
        # Esto asegura que las dependencias se carguen en el orden correcto
        load_order = ['bancos_data.json', 'clientes_data.json', 'creditos_data.json', 'users_data.json']
        
        # Crear diccionario de archivos por nombre
        fixture_dict = {f.name: f for f in all_fixture_files}
        
        # Ordenar según load_order, luego agregar cualquier otro archivo
        fixture_files = []
        for ordered_file in load_order:
            if ordered_file in fixture_dict:
                fixture_files.append(fixture_dict[ordered_file])
        
        # Agregar cualquier otro archivo que no esté en el orden
        for fixture_file in all_fixture_files:
            if fixture_file not in fixture_files:
                fixture_files.append(fixture_file)

        loaded_count = 0
        error_count = 0
        errors = []

        for fixture_file in fixture_files:
            try:
                self.stdout.write(f'Cargando {fixture_file.name}...')
                call_command('loaddata', str(fixture_file), verbosity=2)
                self.stdout.write(self.style.SUCCESS(f'✓ {fixture_file.name} cargado exitosamente'))
                loaded_count += 1
            except Exception as e:
                error_msg = str(e)
                # Verificar diferentes tipos de errores
                if skip_existing and ('already exists' in error_msg.lower() or 'duplicate key' in error_msg.lower()):
                    self.stdout.write(self.style.WARNING(f'⚠ {fixture_file.name} ya existe, omitiendo...'))
                    loaded_count += 1  # Contar como cargado si se omite intencionalmente
                elif 'IntegrityError' in error_msg or 'Foreign key' in error_msg or 'violates foreign key constraint' in error_msg.lower() or 'does not exist' in error_msg.lower():
                    # Error de foreign key - mostrar detalles completos
                    self.stdout.write(self.style.ERROR(f'✗ Error de integridad en {fixture_file.name}:'))
                    self.stdout.write(self.style.ERROR(f'  {error_msg[:500]}'))  # Limitar longitud del mensaje
                    if 'creditos' in fixture_file.name.lower():
                        self.stdout.write(self.style.WARNING('  ⚠ Los créditos requieren que clientes y bancos ya estén cargados'))
                        self.stdout.write(self.style.WARNING('  ⚠ Verifica que los IDs de cliente y banco en créditos existan en la base de datos'))
                    self.stdout.write(self.style.WARNING('  ⚠ Solución: Re-exporta todos los fixtures juntos con: python manage.py export_data'))
                    errors.append(f'{fixture_file.name}: {error_msg[:200]}')
                    error_count += 1
                    # Con skip_existing, continuar pero mostrar el error claramente
                    if not skip_existing:
                        raise CommandError(f'Error de integridad cargando {fixture_file.name}: {error_msg}')
                else:
                    self.stdout.write(self.style.ERROR(f'✗ Error cargando {fixture_file.name}: {error_msg}'))
                    errors.append(f'{fixture_file.name}: {error_msg}')
                    error_count += 1
                    if not skip_existing:
                        raise CommandError(f'Error cargando {fixture_file.name}: {error_msg}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        if error_count == 0:
            self.stdout.write(self.style.SUCCESS(f'✓ {loaded_count} archivo(s) cargado(s) exitosamente!'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ {loaded_count} cargado(s), {error_count} error(es)'))
            self.stdout.write('')
            self.stdout.write(self.style.ERROR('Errores detallados:'))
            for error in errors:
                self.stdout.write(self.style.ERROR(f'  - {error}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
