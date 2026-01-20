"""
ASGI config for tu_credito project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_credito.settings.dev')

application = get_asgi_application()
