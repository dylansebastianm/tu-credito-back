"""
Views for Banco model.
"""
from typing import Optional
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from apps.bancos.models import Banco
from apps.bancos.serializers import BancoSerializer, BancoListSerializer
from apps.bancos.filters import BancoFilter
from apps.bancos.services import BancoService


@extend_schema_view(
    list=extend_schema(
        summary="Listar bancos",
        description="Obtiene una lista paginada de bancos. Permite filtrar por nombre y tipo.",
        tags=['bancos'],
        responses={
            200: BancoListSerializer,
            401: {'description': 'No autenticado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    create=extend_schema(
        summary="Crear banco",
        description="Crea un nuevo banco.",
        tags=['bancos'],
        responses={
            201: BancoSerializer,
            400: {'description': 'Errores de validación'},
            401: {'description': 'No autenticado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    retrieve=extend_schema(
        summary="Obtener banco",
        description="Obtiene los detalles de un banco específico.",
        tags=['bancos'],
        responses={
            200: BancoSerializer,
            401: {'description': 'No autenticado'},
            404: {'description': 'Banco no encontrado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    update=extend_schema(
        summary="Actualizar banco",
        description="Actualiza completamente un banco.",
        tags=['bancos'],
        responses={
            200: BancoSerializer,
            400: {'description': 'Errores de validación'},
            401: {'description': 'No autenticado'},
            404: {'description': 'Banco no encontrado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    partial_update=extend_schema(
        summary="Actualizar banco parcialmente",
        description="Actualiza parcialmente un banco.",
        tags=['bancos'],
        responses={
            200: BancoSerializer,
            400: {'description': 'Errores de validación'},
            401: {'description': 'No autenticado'},
            404: {'description': 'Banco no encontrado'},
            500: {'description': 'Error del servidor'},
        },
    ),
    destroy=extend_schema(
        summary="Eliminar banco",
        description="Elimina un banco. Solo se puede eliminar si no tiene créditos asociados.",
        tags=['bancos'],
        responses={
            204: {'description': 'Banco eliminado exitosamente'},
            400: {'description': 'No se puede eliminar porque tiene créditos asociados'},
            401: {'description': 'No autenticado'},
            404: {'description': 'Banco no encontrado'},
            500: {'description': 'Error del servidor'},
        },
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
