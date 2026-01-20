"""
Filters for Credito model.
"""
import django_filters
from apps.creditos.models import Credito, TipoCredito


class CreditoFilter(django_filters.FilterSet):
    """
    FilterSet para Credito con filtros comunes.
    """
    descripcion = django_filters.CharFilter(lookup_expr='icontains', label='Buscar por descripción')
    tipo_credito = django_filters.ChoiceFilter(choices=TipoCredito.choices, label='Tipo de crédito')
    cliente = django_filters.NumberFilter(field_name='cliente_id', label='Cliente ID')
    banco = django_filters.NumberFilter(field_name='banco_id', label='Banco ID')
    pago_minimo_min = django_filters.NumberFilter(field_name='pago_minimo', lookup_expr='gte', label='Pago mínimo desde')
    pago_minimo_max = django_filters.NumberFilter(field_name='pago_minimo', lookup_expr='lte', label='Pago mínimo hasta')
    pago_maximo_min = django_filters.NumberFilter(field_name='pago_maximo', lookup_expr='gte', label='Pago máximo desde')
    pago_maximo_max = django_filters.NumberFilter(field_name='pago_maximo', lookup_expr='lte', label='Pago máximo hasta')
    plazo_meses_min = django_filters.NumberFilter(field_name='plazo_meses', lookup_expr='gte', label='Plazo mínimo (meses)')
    plazo_meses_max = django_filters.NumberFilter(field_name='plazo_meses', lookup_expr='lte', label='Plazo máximo (meses)')
    fecha_registro_desde = django_filters.DateFilter(field_name='fecha_registro', lookup_expr='gte', label='Fecha registro desde')
    fecha_registro_hasta = django_filters.DateFilter(field_name='fecha_registro', lookup_expr='lte', label='Fecha registro hasta')

    class Meta:
        model = Credito
        fields = [
            'descripcion',
            'tipo_credito',
            'cliente',
            'banco',
            'pago_minimo_min',
            'pago_minimo_max',
            'pago_maximo_min',
            'pago_maximo_max',
            'plazo_meses_min',
            'plazo_meses_max',
            'fecha_registro_desde',
            'fecha_registro_hasta',
        ]
