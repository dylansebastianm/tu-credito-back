"""
Views for Banco model.
"""
from typing import Optional
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.bancos.models import Banco
from apps.bancos.serializers import BancoSerializer, BancoListSerializer
from apps.bancos.filters import BancoFilter
from apps.bancos.services import BancoService


@extend_schema_view(
    list=extend_schema(
        summary="Listar bancos",
        description="Obtiene una lista paginada de bancos. Permite filtrar por nombre y tipo.",
        tags=['bancos'],
    ),
    create=extend_schema(
        summary="Crear banco",
        description="Crea un nuevo banco.",
        tags=['bancos'],
    ),
    retrieve=extend_schema(
        summary="Obtener banco",
        description="Obtiene los detalles de un banco específico.",
        tags=['bancos'],
    ),
    update=extend_schema(
        summary="Actualizar banco",
        description="Actualiza completamente un banco.",
        tags=['bancos'],
    ),
    partial_update=extend_schema(
        summary="Actualizar banco parcialmente",
        description="Actualiza parcialmente un banco.",
        tags=['bancos'],
    ),
    destroy=extend_schema(
        summary="Eliminar banco",
        description="Elimina un banco. Solo se puede eliminar si no tiene créditos asociados.",
        tags=['bancos'],
    ),
)
class BancoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar bancos.
    """
    queryset = Banco.objects.all()
    serializer_class = BancoSerializer
    filterset_class = BancoFilter
    search_fields = ['nombre', 'direccion']
    ordering_fields = ['nombre', 'tipo', 'created_at']
    ordering = ['nombre']

    def get_serializer_class(self):
        """
        Retorna el serializer apropiado según la acción.
        """
        if self.action == 'list':
            return BancoListSerializer
        return BancoSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Eliminar banco con validación de créditos asociados.
        Usa la capa de servicios para separar la lógica de negocio.
        """
        banco = self.get_object()
        
        # Usar el servicio para verificar si se puede eliminar
        result = BancoService.delete_banco_if_safe(banco)
        
        if not result['success']:
            return Response(
                {
                    'error': result['error'],
                    'message': result['message'],
                    'details': result.get('details', {})
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {'message': result['message']},
            status=status.HTTP_204_NO_CONTENT
        )
