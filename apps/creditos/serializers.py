"""
Serializers for Credito model.
"""
from rest_framework import serializers
from apps.creditos.models import Credito, TipoCredito
from apps.clientes.serializers import ClienteListSerializer
from apps.bancos.serializers import BancoListSerializer


class CreditoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Credito.
    """
    tipo_credito_display = serializers.CharField(source='get_tipo_credito_display', read_only=True)
    cliente_info = ClienteListSerializer(source='cliente', read_only=True)
    banco_info = BancoListSerializer(source='banco', read_only=True)

    class Meta:
        model = Credito
        fields = [
            'id',
            'cliente',
            'cliente_info',
            'descripcion',
            'monto',
            'pago_minimo',
            'pago_maximo',
            'plazo_meses',
            'fecha_registro',
            'banco',
            'banco_info',
            'tipo_credito',
            'tipo_credito_display',
            'tasa_interes',
            'cuota_mensual',
            'monto_total',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'fecha_registro', 'cuota_mensual', 'monto_total', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Crear crédito y calcular automáticamente cuota_mensual y monto_total.
        """
        credito = Credito.objects.create(**validated_data)
        # Los cálculos se hacen automáticamente en el método save() del modelo
        return credito
    
    def update(self, instance, validated_data):
        """
        Actualizar crédito y recalcular automáticamente cuota_mensual y monto_total.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # Esto disparará el cálculo automático
        return instance

    def validate_descripcion(self, value):
        """
        Validar que la descripción no esté vacía.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("La descripción no puede estar vacía.")
        return value.strip()

    def validate_tipo_credito(self, value):
        """
        Validar que el tipo de crédito sea válido.
        """
        if value not in TipoCredito.values:
            raise serializers.ValidationError(
                f"El tipo de crédito debe ser uno de: {', '.join(TipoCredito.values)}"
            )
        return value

    def validate_pago_minimo(self, value):
        """
        Validar que el pago mínimo sea positivo.
        """
        if value <= 0:
            raise serializers.ValidationError("El pago mínimo debe ser mayor a 0.")
        return value

    def validate_monto(self, value):
        """
        Validar que el monto sea positivo.
        """
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0.")
        return value

    def validate_pago_maximo(self, value):
        """
        Validar que el pago máximo sea positivo.
        """
        if value <= 0:
            raise serializers.ValidationError("El pago máximo debe ser mayor a 0.")
        return value

    def validate_plazo_meses(self, value):
        """
        Validar que el plazo en meses sea positivo.
        """
        if value <= 0:
            raise serializers.ValidationError("El plazo en meses debe ser mayor a 0.")
        return value

    def validate_tasa_interes(self, value):
        """
        Validar que la tasa de interés sea positiva.
        """
        if value <= 0:
            raise serializers.ValidationError("La tasa de interés debe ser mayor a 0.")
        return value

    def validate(self, attrs):
        """
        Validar que pago_minimo <= pago_maximo.
        """
        pago_minimo = attrs.get('pago_minimo', getattr(self.instance, 'pago_minimo', None))
        pago_maximo = attrs.get('pago_maximo', getattr(self.instance, 'pago_maximo', None))
        
        if pago_minimo and pago_maximo:
            if pago_minimo > pago_maximo:
                raise serializers.ValidationError(
                    {
                        'pago_maximo': 'El pago máximo debe ser mayor o igual al pago mínimo.'
                    }
                )
        
        return attrs


class CreditoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de créditos.
    """
    tipo_credito_display = serializers.CharField(source='get_tipo_credito_display', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre_completo', read_only=True)
    banco_nombre = serializers.CharField(source='banco.nombre', read_only=True)

    class Meta:
        model = Credito
        fields = [
            'id',
            'cliente_nombre',
            'descripcion',
            'monto',
            'pago_minimo',
            'pago_maximo',
            'plazo_meses',
            'fecha_registro',
            'banco_nombre',
            'tipo_credito',
            'tipo_credito_display',
            'tasa_interes',
            'cuota_mensual',
            'monto_total',
        ]
