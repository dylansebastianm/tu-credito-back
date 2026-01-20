"""
Views for Credito model.
"""
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.creditos.models import Credito
from apps.creditos.serializers import CreditoSerializer, CreditoListSerializer
from apps.creditos.filters import CreditoFilter


@extend_schema_view(
    list=extend_schema(
        summary="Listar créditos",
        description="Obtiene una lista paginada de créditos. Permite filtrar por múltiples criterios.",
        tags=['creditos'],
    ),
    create=extend_schema(
        summary="Crear crédito",
        description="Crea un nuevo crédito. Se enviará un email de confirmación al cliente.",
        tags=['creditos'],
    ),
    retrieve=extend_schema(
        summary="Obtener crédito",
        description="Obtiene los detalles de un crédito específico.",
        tags=['creditos'],
    ),
    update=extend_schema(
        summary="Actualizar crédito",
        description="Actualiza completamente un crédito.",
        tags=['creditos'],
    ),
    partial_update=extend_schema(
        summary="Actualizar crédito parcialmente",
        description="Actualiza parcialmente un crédito.",
        tags=['creditos'],
    ),
    destroy=extend_schema(
        summary="Eliminar crédito",
        description="Elimina un crédito.",
        tags=['creditos'],
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
