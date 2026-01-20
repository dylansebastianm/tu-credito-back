"""
Core views for Tu Crédito API
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers as drf_serializers
from rest_framework_simplejwt.views import TokenViewBase
from apps.core.serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    EmailTokenObtainPairSerializer
)

User = get_user_model()


class EmailTokenObtainPairView(TokenViewBase):
    """
    Vista personalizada para obtener tokens JWT usando email en lugar de username.
    """
    serializer_class = EmailTokenObtainPairSerializer

    @extend_schema(
        request=inline_serializer(
            name='EmailLoginRequest',
            fields={
                'email': drf_serializers.EmailField(),
                'password': drf_serializers.CharField(style={'input_type': 'password'}),
            }
        ),
        responses={
            200: inline_serializer(
                name='TokenResponse',
                fields={
                    'access': drf_serializers.CharField(),
                    'refresh': drf_serializers.CharField(),
                }
            ),
            401: {'description': 'Credenciales inválidas'}
        },
        description='Obtiene tokens JWT (access y refresh) usando email y contraseña.',
        tags=['Autenticación']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class HealthCheckView(APIView):
    """
    Health check endpoint para verificar el estado del sistema.
    No requiere autenticación.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                'status': 'healthy',
                'service': 'Tu Crédito API',
                'version': '1.0.0',
            },
            status=status.HTTP_200_OK
        )


class CurrentUserView(APIView):
    """
    Endpoint para obtener información del usuario autenticado.
    Requiere autenticación JWT.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer},
        description='Retorna información del usuario actual basado en el token JWT.',
        tags=['Autenticación']
    )
    def get(self, request):
        """
        Retorna información del usuario actual basado en el token JWT.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    Endpoint para registrar nuevos usuarios.
    Requiere autenticación y que el usuario sea superusuario.
    Las contraseñas se hashean automáticamente por Django.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={
            201: inline_serializer(
                name='RegisterResponse',
                fields={
                    'message': drf_serializers.CharField(),
                    'user': UserSerializer(),
                }
            ),
            400: {'description': 'Errores de validación'},
            403: {'description': 'No tienes permisos (solo superusuarios)'}
        },
        description='Crea un nuevo usuario. Solo los superusuarios pueden crear usuarios. La contraseña se hashea automáticamente antes de guardar en la BD.',
        tags=['auth']
    )
    def post(self, request):
        """
        Crea un nuevo usuario.
        Solo los superusuarios pueden crear usuarios.
        La contraseña se hashea automáticamente antes de guardar en la BD.
        """
        # Verificar que el usuario sea superusuario
        if not request.user.is_superuser:
            return Response(
                {
                    'error': 'No tienes permisos para realizar esta acción.',
                    'detail': 'Solo los superusuarios pueden crear usuarios.'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            # Retornar información del usuario (sin contraseña)
            user_data = UserSerializer(user).data
            return Response(
                {
                    'message': 'Usuario creado exitosamente',
                    'user': user_data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
