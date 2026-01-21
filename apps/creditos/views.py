"""
Views for Credito model.
"""
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from apps.creditos.models import Credito
from apps.creditos.serializers import CreditoSerializer, CreditoListSerializer
from apps.creditos.filters import CreditoFilter


@extend_schema_view(
    list=extend_schema(
        summary="Listar créditos",
        description="Obtiene una lista paginada de créditos. Permite filtrar por múltiples criterios.",
        tags=['creditos'],
        responses={
            200: CreditoListSerializer,
            401: {'description': 'No autenticado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    create=extend_schema(
        summary="Crear crédito",
        description="Crea un nuevo crédito. Se enviará un email de confirmación al cliente.",
        tags=['creditos'],
        responses={
            201: CreditoSerializer,
            400: {'description': 'Errores de validación'},
            401: {'description': 'No autenticado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    retrieve=extend_schema(
        summary="Obtener crédito",
        description="Obtiene los detalles de un crédito específico.",
        tags=['creditos'],
        responses={
            200: CreditoSerializer,
            401: {'description': 'No autenticado'},
            404: {'description': 'Crédito no encontrado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    update=extend_schema(
        summary="Actualizar crédito",
        description="Actualiza completamente un crédito.",
        tags=['creditos'],
        responses={
            200: CreditoSerializer,
            400: {'description': 'Errores de validación'},
            401: {'description': 'No autenticado'},
            404: {'description': 'Crédito no encontrado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    partial_update=extend_schema(
        summary="Actualizar crédito parcialmente",
        description="Actualiza parcialmente un crédito.",
        tags=['creditos'],
        responses={
            200: CreditoSerializer,
            400: {'description': 'Errores de validación'},
            401: {'description': 'No autenticado'},
            404: {'description': 'Crédito no encontrado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    destroy=extend_schema(
        summary="Eliminar crédito",
        description="Elimina un crédito.",
        tags=['creditos'],
        responses={
            204: {'description': 'Crédito eliminado exitosamente'},
            401: {'description': 'No autenticado'},
            404: {'description': 'Crédito no encontrado'},
            500: {'description': 'Error del servidor'},
        },
    ),
)
class CreditoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar créditos.
    """
    queryset = Credito.objects.select_related('cliente', 'banco').all()
    serializer_class = CreditoSerializer
    filterset_class = CreditoFilter
    search_fields = ['descripcion', 'cliente__nombre_completo', 'banco__nombre']
    ordering_fields = [
        'fecha_registro',
        'pago_minimo',
        'pago_maximo',
        'plazo_meses',
        'tipo_credito',
        'created_at',
    ]
    ordering = ['-fecha_registro']

    def get_serializer_class(self):
        """
        Retorna el serializer apropiado según la acción.
        """
        if self.action == 'list':
            return CreditoListSerializer
        return CreditoSerializer
