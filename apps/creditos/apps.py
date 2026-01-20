from django.apps import AppConfig


class CreditosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.creditos'

    def ready(self):
        """Importar señales cuando la app está lista."""
        import apps.creditos.signals  # noqa
