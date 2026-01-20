"""
Development settings for tu_credito project.
"""
from .base import *

DEBUG = True

INSTALLED_APPS += [
    # Development apps
]

# Allow CORS for development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# Development logging - INFO level for cleaner API development
# Shows HTTP requests, errors, and important info without DEBUG verbosity
LOGGING['root']['level'] = 'INFO'
LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['django.request'] = {
    'handlers': ['console'],
    'level': 'INFO',
    'propagate': False,
}
LOGGING['loggers']['django.server'] = {
    'handlers': ['console'],
    'level': 'INFO',
    'propagate': False,
}
LOGGING['loggers']['apps']['level'] = 'INFO'
