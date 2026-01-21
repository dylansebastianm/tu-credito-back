"""
Views for Credito model.
"""
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers as drf_serializers
from apps.creditos.models import Credito
from apps.creditos.serializers import CreditoSerializer, CreditoListSerializer
from apps.creditos.filters import CreditoFilter


# Helper para crear serializers de error consistentes
def get_error_response_serializer(status_code: int, name_suffix: str = ''):
    """Crea un serializer inline para respuestas de error."""
    return inline_serializer(
        name=f'Error{status_code}{name_suffix}',
        fields={
            'error': drf_serializers.BooleanField(default=True),
            'message': drf_serializers.CharField(),
            'details': drf_serializers.DictField(),
            'status_code': drf_serializers.IntegerField(default=status_code),
        }
    )


@extend_schema_view(
    list=extend_schema(
        summary="Listar créditos",
        description="Obtiene una lista paginada de créditos. Permite filtrar por múltiples criterios.",
        tags=['creditos'],
        responses={
            200: CreditoListSerializer,
            401: get_error_response_serializer(401),
            500: get_error_response_serializer(500),
        },
    ),
    create=extend_schema(
        summary="Crear crédito",
        description="Crea un nuevo crédito. Se enviará un email de confirmación al cliente.",
        tags=['creditos'],
        responses={
            201: CreditoSerializer,
            400: get_error_response_serializer(400),
            401: get_error_response_serializer(401),
            500: get_error_response_serializer(500),
        },
    ),
    retrieve=extend_schema(
        summary="Obtener crédito",
        description="Obtiene los detalles de un crédito específico.",
        tags=['creditos'],
        responses={
            200: CreditoSerializer,
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
    update=extend_schema(
        summary="Actualizar crédito",
        description="Actualiza completamente un crédito.",
        tags=['creditos'],
        responses={
            200: CreditoSerializer,
            400: get_error_response_serializer(400),
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
    partial_update=extend_schema(
        summary="Actualizar crédito parcialmente",
        description="Actualiza parcialmente un crédito.",
        tags=['creditos'],
        responses={
            200: CreditoSerializer,
            400: get_error_response_serializer(400),
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
    destroy=extend_schema(
        summary="Eliminar crédito",
        description="Elimina un crédito.",
        tags=['creditos'],
        responses={
            204: None,
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
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
