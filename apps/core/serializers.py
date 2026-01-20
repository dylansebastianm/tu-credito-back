"""
Serializers for core app - Authentication
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de nuevos usuarios.
    Las contraseñas se hashean automáticamente por Django.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="Contraseña del usuario (se hashea automáticamente antes de guardar)"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Confirmación de la contraseña"
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password_confirm',
            'is_staff',
            'is_superuser',
        ]
        read_only_fields = ['id', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        """
        Valida que las contraseñas coincidan.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Las contraseñas no coinciden.'
            })
        return attrs

    def validate_username(self, value):
        """
        Valida que el username no exista.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Este nombre de usuario ya está en uso.')
        return value

    def validate_email(self, value):
        """
        Valida que el email no exista (si se proporciona).
        """
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este email ya está registrado.')
        return value

    def create(self, validated_data):
        """
        Crea un nuevo usuario con contraseña hasheada.
        Django hashea automáticamente la contraseña con set_password().
        """
        validated_data.pop('password_confirm')  # No se guarda la confirmación
        password = validated_data.pop('password')
        
        # Crear usuario sin contraseña primero
        user = User.objects.create(**validated_data)
        
        # Establecer contraseña (Django la hashea automáticamente)
        user.set_password(password)
        user.save()
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para obtener información de usuario (sin contraseña).
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'date_joined',
        ]
        read_only_fields = ['id', 'date_joined']


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para obtener tokens JWT usando email en lugar de username.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remover el campo username del serializer base
        self.fields.pop('username', None)

    def validate(self, attrs):
        """
        Valida las credenciales usando email en lugar de username.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Buscar usuario por email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {'email': 'No existe una cuenta con este email.'},
                    code='authorization'
                )

            # Autenticar con username (porque Django usa username internamente)
            user = authenticate(
                request=self.context.get('request'),
                username=user.username,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    {'password': 'Contraseña incorrecta.'},
                    code='authorization'
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    {'email': 'Esta cuenta está desactivada.'},
                    code='authorization'
                )

            # Establecer el usuario para que el serializer base pueda usarlo
            self.user = user

            # Generar tokens usando el método del serializer base
            refresh = self.get_token(user)
            
            # Retornar solo access y refresh (formato esperado por TokenViewBase)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        raise serializers.ValidationError(
            {'email': 'Debe proporcionar email y contraseña.'},
            code='authorization'
        )
