"""
Filters for Banco model.
"""
import django_filters
from apps.bancos.models import Banco, TipoBanco


class BancoFilter(django_filters.FilterSet):
    """
    FilterSet para Banco con filtros comunes.
    """
    nombre = django_filters.CharFilter(lookup_expr='icontains', label='Buscar por nombre')
    tipo = django_filters.ChoiceFilter(choices=TipoBanco.choices, label='Tipo de banco')

    class Meta:
        model = Banco
        fields = ['nombre', 'tipo']
