"""
Core views for tu_credito project.
"""
from typing import Dict, Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from django.db import connection
from drf_spectacular.utils import extend_schema


class HealthCheckView(APIView):
    """
    Health check endpoint para verificar el estado del sistema.
    """
    permission_classes = []  # No requiere autenticación
    
    @extend_schema(
        summary="Health check",
        description="Verifica el estado del sistema y la conexión a la base de datos",
        tags=['health'],
        responses={
            200: {
                'description': 'Sistema operativo',
                'type': 'object',
            },
            503: {
                'description': 'Sistema no disponible',
                'type': 'object',
            },
        },
    )
    def get(self, request: Request) -> Response:
        """
        Verifica el estado del sistema.
        
        Args:
            request: Request object de DRF
            
        Returns:
            Response: Respuesta con el estado del sistema
        """
        try:
            # Verificar conexión a la base de datos
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            return Response(
                {
                    'status': 'healthy',
                    'database': 'connected',
                    'service': 'tu_credito_api',
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'status': 'unhealthy',
                    'database': 'disconnected',
                    'error': str(e),
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
