"""
Comando para exportar datos de la base de datos a fixtures JSON.
Uso: python manage.py export_data [app_name]
Si no se especifica app_name, exporta todas las apps.
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
import os
import io
from pathlib import Path


class Command(BaseCommand):
    help = 'Exporta datos de la base de datos a archivos JSON (fixtures). Uso: python manage.py export_data [app_name]'

    def add_arguments(self, parser):
        parser.add_argument(
            'app_name',
            nargs='?',
            type=str,
            help='Nombre de la app a exportar (opcional). Si no se especifica, exporta todas las apps.',
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='fixtures',
            help='Directorio donde guardar los fixtures (default: fixtures)',
        )

    def handle(self, *args, **options):
        app_name = options.get('app_name', None)
        output_dir = options.get('output_dir', 'fixtures')

        # Crear directorio de fixtures si no existe
        fixtures_path = Path(output_dir)
        fixtures_path.mkdir(exist_ok=True)

        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Exportando datos a fixtures'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')

        def export_to_file(app_or_model, output_path):
            """Helper para exportar datos a un archivo con encoding UTF-8 explícito"""
            # Leer datos usando dumpdata a un StringIO
            from django.core import serializers
            from django.apps import apps
            
            # Obtener el modelo o app
            if '.' in app_or_model:
                # Es un modelo específico (ej: auth.user)
                app_label, model_name = app_or_model.split('.', 1)
                model = apps.get_model(app_label, model_name)
                queryset = model.objects.all()
            else:
                # Es una app completa
                app = apps.get_app_config(app_or_model)
                queryset = None
                models = app.get_models()
            
            # Serializar a JSON con encoding UTF-8
            if queryset is not None:
                # Modelo específico
                data = serializers.serialize('json', queryset, indent=2, ensure_ascii=False)
            else:
                # App completa - serializar todos los modelos
                objects = []
                for model in models:
                    objects.extend(model.objects.all())
                data = serializers.serialize('json', objects, indent=2, ensure_ascii=False)
            
            # Escribir en UTF-8 explícitamente
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(data)
        
        try:
            if app_name:
                # Exportar una app específica
                output_file = fixtures_path / f'{app_name}_data.json'
                export_to_file(app_name, output_file)
                self.stdout.write(self.style.SUCCESS(f'✓ Datos de {app_name} exportados a {output_file}'))
            else:
                # Exportar todas las apps del proyecto
                apps_to_export = ['bancos', 'clientes', 'creditos']
                for app in apps_to_export:
                    output_file = fixtures_path / f'{app}_data.json'
                    try:
                        export_to_file(app, output_file)
                        # Verificar si el archivo tiene contenido (más que solo [])
                        if output_file.exists() and output_file.stat().st_size > 10:
                            self.stdout.write(self.style.SUCCESS(f'✓ Datos de {app} exportados a {output_file}'))
                        else:
                            # Eliminar archivo vacío
                            output_file.unlink(missing_ok=True)
                            self.stdout.write(self.style.WARNING(f'⚠ {app} no tiene datos para exportar'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'✗ Error exportando {app}: {str(e)}'))
                
                # Exportar usuarios (auth.user)
                output_file = fixtures_path / 'users_data.json'
                try:
                    export_to_file('auth.user', output_file)
                    # Verificar si el archivo tiene contenido (más que solo [])
                    if output_file.exists() and output_file.stat().st_size > 10:
                        self.stdout.write(self.style.SUCCESS(f'✓ Usuarios exportados a {output_file}'))
                    else:
                        # Eliminar archivo vacío
                        output_file.unlink(missing_ok=True)
                        self.stdout.write(self.style.WARNING('⚠ No hay usuarios para exportar'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ Error exportando usuarios: {str(e)}'))

            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 50))
            self.stdout.write(self.style.SUCCESS('Exportación completada!'))
            self.stdout.write(self.style.SUCCESS('=' * 50))
            self.stdout.write('')
            self.stdout.write(f'Los fixtures están en: {fixtures_path.absolute()}')
            self.stdout.write('')
            self.stdout.write('Para cargar estos datos en producción, usa:')
            self.stdout.write('  python manage.py loaddata fixtures/*_data.json')
            self.stdout.write('')

        except CommandError as e:
            self.stdout.write(self.style.ERROR('=' * 50))
            self.stdout.write(self.style.ERROR('ERROR: La exportación falló'))
            self.stdout.write(self.style.ERROR(str(e)))
            self.stdout.write(self.style.ERROR('=' * 50))
            raise
