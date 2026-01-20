"""
Serializers for Cliente model.
"""
from rest_framework import serializers
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from apps.clientes.models import Cliente, TipoPersona
from apps.bancos.serializers import BancoListSerializer


class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Cliente.
    """
    tipo_persona_display = serializers.CharField(source='get_tipo_persona_display', read_only=True)
    banco_info = BancoListSerializer(source='banco', read_only=True)

    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre_completo',
            'fecha_nacimiento',
            'edad',
            'nacionalidad',
            'direccion',
            'email',
            'telefono',
            'tipo_persona',
            'tipo_persona_display',
            'banco',
            'banco_info',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'edad', 'created_at', 'updated_at']

    def validate_nombre_completo(self, value):
        """
        Validar que el nombre completo no esté vacío.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre completo no puede estar vacío.")
        return value.strip()

    def validate_fecha_nacimiento(self, value):
        """
        Validar que la fecha de nacimiento sea válida.
        """
        if value and value > timezone.now().date():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
        return value

    def validate_tipo_persona(self, value):
        """
        Validar que el tipo de persona sea válido.
        """
        if value not in TipoPersona.values:
            raise serializers.ValidationError(
                f"El tipo de persona debe ser uno de: {', '.join(TipoPersona.values)}"
            )
        return value

    def validate_email(self, value):
        """
        Validar formato de email.
        """
        if not value or '@' not in value:
            raise serializers.ValidationError("Debe proporcionar un email válido.")
        return value.lower().strip()

    def validate(self, attrs):
        """
        Validar que la edad coincida con la fecha de nacimiento.
        """
        fecha_nacimiento = attrs.get('fecha_nacimiento', getattr(self.instance, 'fecha_nacimiento', None))
        
        if fecha_nacimiento:
            today = timezone.now().date()
            calculated_age = relativedelta(today, fecha_nacimiento).years
            
            # Si se está creando o actualizando la edad
            edad = attrs.get('edad', getattr(self.instance, 'edad', None))
            
            if edad is not None and edad != calculated_age:
                raise serializers.ValidationError(
                    {
                        'edad': f'La edad debe ser {calculated_age} según la fecha de nacimiento.'
                    }
                )
            
            # Calcular edad automáticamente si no se proporciona
            if 'edad' not in attrs:
                attrs['edad'] = calculated_age
        
        return attrs


class ClienteListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de clientes.
    """
    tipo_persona_display = serializers.CharField(source='get_tipo_persona_display', read_only=True)

    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre_completo',
            'email',
            'telefono',
            'edad',
            'tipo_persona',
            'tipo_persona_display',
        ]
