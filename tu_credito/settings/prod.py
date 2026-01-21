"""
Production settings for tu_credito project.
"""
from .base import *

DEBUG = False

# Security settings for production
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS configuration for production
# Permitir peticiones desde el frontend en Vercel
# Se puede configurar mediante variable de entorno CORS_ALLOWED_ORIGINS (separados por comas)
# O usar el valor por defecto
cors_origins = env.list('CORS_ALLOWED_ORIGINS', default=[
    "https://tu-credito-front.vercel.app",
])
CORS_ALLOWED_ORIGINS = cors_origins

CORS_ALLOW_CREDENTIALS = True

# CORS headers configuration
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Production logging
# En Render, los logs se capturan automáticamente desde la consola
# No necesitamos archivos de log, Render los maneja
LOGGING['root']['handlers'] = ['console']
LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['apps']['handlers'] = ['console']

# CSP para producción - activar upgrade insecure requests
CSP_UPGRADE_INSECURE_REQUESTS = True
