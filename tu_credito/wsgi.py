"""
WSGI config for tu_credito project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_credito.settings.dev')

application = get_wsgi_application()
