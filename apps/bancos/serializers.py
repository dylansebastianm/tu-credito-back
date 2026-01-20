"""
Serializers for Banco model.
"""
from rest_framework import serializers
from apps.bancos.models import Banco, TipoBanco


class BancoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Banco.
    """
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Banco
        fields = [
            'id',
            'nombre',
            'tipo',
            'tipo_display',
            'direccion',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_nombre(self, value):
        """
        Validar que el nombre no esté vacío.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del banco no puede estar vacío.")
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


class BancoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de bancos.
    """
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Banco
        fields = ['id', 'nombre', 'tipo', 'tipo_display', 'direccion']
