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
        Validar que la fecha de nacimiento sea válida y que el cliente sea mayor de edad (18+).
        """
        if value and value > timezone.now().date():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
        
        # Validar que el cliente sea mayor de edad (18 años o más)
        if value:
            today = timezone.now().date()
            calculated_age = relativedelta(today, value).years
            
            if calculated_age < 18:
                raise serializers.ValidationError(
                    f"El cliente debe ser mayor de edad (18 años o más). La fecha de nacimiento resulta en una edad de {calculated_age} años."
                )
            
            if calculated_age > 99:
                raise serializers.ValidationError(
                    f"La fecha de nacimiento resulta en una edad inválida ({calculated_age} años). La edad debe estar entre 18 y 99 años."
                )
        
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
        Validar formato de email y unicidad.
        """
        if not value or '@' not in value:
            raise serializers.ValidationError("Debe proporcionar un email válido.")
        
        value = value.lower().strip()
        
        # Validar unicidad del email
        # Si estamos editando (self.instance existe), excluir el registro actual
        queryset = Cliente.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("Este email ya está registrado por otro cliente.")
        
        return value

    def validate_telefono(self, value):
        """
        Validar unicidad del teléfono.
        """
        # Si el teléfono está vacío o es None, permitirlo (es requerido en frontend pero puede ser None en backend)
        if not value or not value.strip():
            return value if value is None else (value.strip() if value.strip() else None)
        
        value = value.strip()
        
        # Normalizar el teléfono para comparación (remover espacios, guiones, paréntesis, pero mantener +)
        import re
        normalized_phone = re.sub(r'[\s\-\(\)]', '', value)
        
        # Validar unicidad del teléfono normalizado
        # Si estamos editando (self.instance existe), excluir el registro actual
        # Obtener todos los clientes con teléfono (excluyendo null y vacíos)
        queryset = Cliente.objects.exclude(telefono__isnull=True).exclude(telefono='')
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        # Verificar si algún teléfono existente, al normalizarlo, coincide
        # Esto es necesario porque los teléfonos pueden estar almacenados en diferentes formatos
        for cliente in queryset:
            if cliente.telefono:
                existing_normalized = re.sub(r'[\s\-\(\)]', '', cliente.telefono)
                if existing_normalized == normalized_phone:
                    raise serializers.ValidationError("Este teléfono ya está registrado por otro cliente.")
        
        return value

    def validate(self, attrs):
        """
        Validar datos del cliente.
        La edad es read_only y se calcula automáticamente en el modelo basándose en fecha_nacimiento.
        No se debe enviar desde el frontend.
        """
        # La edad es read_only, así que no debería estar en attrs
        # Si está presente, eliminarla ya que se calculará automáticamente en el modelo.save()
        if 'edad' in attrs:
            del attrs['edad']
        
        # La edad se calculará automáticamente en el modelo.save() basándose en fecha_nacimiento
        # El modelo tiene su propia validación en el método clean() que verifica la coherencia
        
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
