"""
Filters for Cliente model.
"""
import django_filters
from apps.clientes.models import Cliente, TipoPersona


class ClienteFilter(django_filters.FilterSet):
    """
    FilterSet para Cliente con filtros comunes.
    """
    nombre_completo = django_filters.CharFilter(lookup_expr='icontains', label='Buscar por nombre')
    email = django_filters.CharFilter(lookup_expr='icontains', label='Buscar por email')
    tipo_persona = django_filters.ChoiceFilter(choices=TipoPersona.choices, label='Tipo de persona')
    edad_min = django_filters.NumberFilter(field_name='edad', lookup_expr='gte', label='Edad mínima')
    edad_max = django_filters.NumberFilter(field_name='edad', lookup_expr='lte', label='Edad máxima')
    banco = django_filters.NumberFilter(field_name='banco_id', label='Banco ID')

    class Meta:
        model = Cliente
        fields = ['nombre_completo', 'email', 'tipo_persona', 'edad_min', 'edad_max', 'banco']
