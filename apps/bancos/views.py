"""
Views for Banco model.
"""
from typing import Optional
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers as drf_serializers
from apps.bancos.models import Banco
from apps.bancos.serializers import BancoSerializer, BancoListSerializer
from apps.bancos.filters import BancoFilter
from apps.bancos.services import BancoService


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
        summary="Listar bancos",
        description="Obtiene una lista paginada de bancos. Permite filtrar por nombre y tipo.",
        tags=['bancos'],
        responses={
            200: BancoListSerializer,
            401: get_error_response_serializer(401),
            500: get_error_response_serializer(500),
        },
    ),
    create=extend_schema(
        summary="Crear banco",
        description="Crea un nuevo banco.",
        tags=['bancos'],
        responses={
            201: BancoSerializer,
            400: get_error_response_serializer(400),
            401: get_error_response_serializer(401),
            500: get_error_response_serializer(500),
        },
    ),
    retrieve=extend_schema(
        summary="Obtener banco",
        description="Obtiene los detalles de un banco específico.",
        tags=['bancos'],
        responses={
            200: BancoSerializer,
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
    update=extend_schema(
        summary="Actualizar banco",
        description="Actualiza completamente un banco.",
        tags=['bancos'],
        responses={
            200: BancoSerializer,
            400: get_error_response_serializer(400),
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
    partial_update=extend_schema(
        summary="Actualizar banco parcialmente",
        description="Actualiza parcialmente un banco.",
        tags=['bancos'],
        responses={
            200: BancoSerializer,
            400: get_error_response_serializer(400),
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
    destroy=extend_schema(
        summary="Eliminar banco",
        description="Elimina un banco. Solo se puede eliminar si no tiene créditos asociados.",
        tags=['bancos'],
        responses={
            204: None,
            400: get_error_response_serializer(400, 'Delete'),
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
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
