"""
Views for Cliente model.
"""
from typing import Optional
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers as drf_serializers
from apps.clientes.models import Cliente
from apps.clientes.serializers import ClienteSerializer, ClienteListSerializer
from apps.clientes.filters import ClienteFilter
from apps.clientes.services import ClienteService


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
        summary="Listar clientes",
        description="Obtiene una lista paginada de clientes. Permite filtrar por nombre, email, tipo de persona, edad y banco.",
        tags=['clientes'],
        responses={
            200: ClienteListSerializer,
            401: get_error_response_serializer(401),
            500: get_error_response_serializer(500),
        },
    ),
    create=extend_schema(
        summary="Crear cliente",
        description="Crea un nuevo cliente. La edad se calcula automáticamente según la fecha de nacimiento.",
        tags=['clientes'],
        responses={
            201: ClienteSerializer,
            400: get_error_response_serializer(400),
            401: get_error_response_serializer(401),
            500: get_error_response_serializer(500),
        },
    ),
    retrieve=extend_schema(
        summary="Obtener cliente",
        description="Obtiene los detalles de un cliente específico.",
        tags=['clientes'],
        responses={
            200: ClienteSerializer,
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
    update=extend_schema(
        summary="Actualizar cliente",
        description="Actualiza completamente un cliente.",
        tags=['clientes'],
        responses={
            200: ClienteSerializer,
            400: get_error_response_serializer(400),
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
    partial_update=extend_schema(
        summary="Actualizar cliente parcialmente",
        description="Actualiza parcialmente un cliente. La edad se recalcula automáticamente si se actualiza la fecha de nacimiento.",
        tags=['clientes'],
        responses={
            200: ClienteSerializer,
            400: get_error_response_serializer(400),
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
    destroy=extend_schema(
        summary="Eliminar cliente",
        description="Elimina un cliente. Solo se puede eliminar si no tiene créditos asociados.",
        tags=['clientes'],
        responses={
            204: None,
            400: get_error_response_serializer(400, 'Delete'),
            401: get_error_response_serializer(401),
            404: get_error_response_serializer(404),
            500: get_error_response_serializer(500),
        },
    ),
)
class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar clientes.
    """
    queryset = Cliente.objects.select_related('banco').all()
    serializer_class = ClienteSerializer
    filterset_class = ClienteFilter
    search_fields = ['nombre_completo', 'email', 'telefono', 'direccion']
    ordering_fields = ['nombre_completo', 'email', 'edad', 'fecha_nacimiento', 'created_at']
    ordering = ['nombre_completo']

    def get_serializer_class(self):
        """
        Retorna el serializer apropiado según la acción.
        """
        if self.action == 'list':
            return ClienteListSerializer
        return ClienteSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Eliminar cliente con validación de créditos asociados.
        Usa la capa de servicios para separar la lógica de negocio.
        """
        cliente = self.get_object()
        
        # Usar el servicio para verificar si se puede eliminar
        result = ClienteService.delete_cliente_if_safe(cliente)
        
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
