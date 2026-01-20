"""
Serializers for Banco model.
"""
from rest_framework import serializers
from apps.bancos.models import Banco, TipoBanco, EstadoBanco


class BancoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Banco.
    """
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    creditos_activos = serializers.SerializerMethodField()

    class Meta:
        model = Banco
        fields = [
            'id',
            'nombre',
            'codigo',
            'tipo',
            'tipo_display',
            'direccion',
            'email',
            'telefono',
            'sitio_web',
            'tasa_interes_min',
            'tasa_interes_max',
            'plazo_minimo',
            'plazo_maximo',
            'monto_minimo',
            'monto_maximo',
            'estado',
            'estado_display',
            'creditos_activos',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'creditos_activos']

    def get_creditos_activos(self, obj):
        """Contar créditos activos asociados a este banco."""
        from apps.creditos.models import Credito
        return Credito.objects.filter(banco=obj).count()

    def validate_nombre(self, value):
        """
        Validar que el nombre no esté vacío.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del banco no puede estar vacío.")
        return value.strip()

    def validate_codigo(self, value):
        """
        Validar que el código no esté vacío.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El código del banco no puede estar vacío.")
        return value.strip()

    def validate_tipo(self, value):
        """
        Validar que el tipo sea válido.
        """
        if value not in TipoBanco.values:
            raise serializers.ValidationError(
                f"El tipo debe ser uno de: {', '.join(TipoBanco.values)}"
            )
        return value

    def validate_estado(self, value):
        """
        Validar que el estado sea válido.
        """
        if value not in EstadoBanco.values:
            raise serializers.ValidationError(
                f"El estado debe ser uno de: {', '.join(EstadoBanco.values)}"
            )
        return value

    def validate_email(self, value):
        """
        Validar formato de email.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El email es requerido.")
        if '@' not in value:
            raise serializers.ValidationError("Debe proporcionar un email válido.")
        return value.lower().strip()

    def validate_telefono(self, value):
        """
        Validar teléfono.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El teléfono es requerido.")
        # Validar que tenga entre 10 y 15 dígitos (después de limpiar)
        import re
        cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
        if len(cleaned) < 10 or len(cleaned) > 15:
            raise serializers.ValidationError("El teléfono debe tener entre 10 y 15 dígitos.")
        return value.strip()

    def validate_direccion(self, value):
        """
        Validar dirección.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("La dirección es requerida.")
        return value.strip()

    def validate(self, attrs):
        """
        Validaciones cruzadas.
        """
        # Validar que tasa_interes_min <= tasa_interes_max
        tasa_min = attrs.get('tasa_interes_min') or (self.instance.tasa_interes_min if self.instance else None)
        tasa_max = attrs.get('tasa_interes_max') or (self.instance.tasa_interes_max if self.instance else None)
        if tasa_min and tasa_max and tasa_min > tasa_max:
            raise serializers.ValidationError({
                'tasa_interes_max': 'La tasa máxima debe ser mayor o igual a la tasa mínima.'
            })

        # Validar que plazo_minimo <= plazo_maximo
        plazo_min = attrs.get('plazo_minimo') or (self.instance.plazo_minimo if self.instance else None)
        plazo_max = attrs.get('plazo_maximo') or (self.instance.plazo_maximo if self.instance else None)
        if plazo_min and plazo_max and plazo_min > plazo_max:
            raise serializers.ValidationError({
                'plazo_maximo': 'El plazo máximo debe ser mayor o igual al plazo mínimo.'
            })

        # Validar que monto_minimo <= monto_maximo
        monto_min = attrs.get('monto_minimo') or (self.instance.monto_minimo if self.instance else None)
        monto_max = attrs.get('monto_maximo') or (self.instance.monto_maximo if self.instance else None)
        if monto_min and monto_max and monto_min > monto_max:
            raise serializers.ValidationError({
                'monto_maximo': 'El monto máximo debe ser mayor o igual al monto mínimo.'
            })

        return attrs


class BancoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de bancos.
    """
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    creditos_activos = serializers.SerializerMethodField()

    class Meta:
        model = Banco
        fields = [
            'id',
            'nombre',
            'codigo',
            'tipo',
            'tipo_display',
            'tasa_interes_min',
            'tasa_interes_max',
            'estado',
            'estado_display',
            'creditos_activos',
        ]

    def get_creditos_activos(self, obj):
        """Contar créditos activos asociados a este banco."""
        from apps.creditos.models import Credito
        return Credito.objects.filter(banco=obj).count()
