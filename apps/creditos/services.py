"""
Services layer for Credito business logic.
Separates business logic from views and models for better architecture.
"""
from typing import Optional, Dict, Any
from decimal import Decimal
from django.db import models
from apps.creditos.models import Credito, TipoCredito


class CreditoService:
    """
    Service class for Credito business logic operations.
    """
    
    @staticmethod
    def validate_payment_range(pago_minimo: Decimal, pago_maximo: Decimal) -> bool:
        """
        Valida que el pago mínimo sea menor o igual al pago máximo.
        
        Args:
            pago_minimo: Pago mínimo del crédito
            pago_maximo: Pago máximo del crédito
            
        Returns:
            True si es válido, False en caso contrario
        """
        return pago_minimo <= pago_maximo
    
    @staticmethod
    def validate_credit_data(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Valida los datos de un crédito antes de crear/actualizar.
        
        Args:
            data: Diccionario con los datos del crédito
            
        Returns:
            Tuple (is_valid: bool, error_message: Optional[str])
        """
        pago_minimo = data.get('pago_minimo')
        pago_maximo = data.get('pago_maximo')
        
        if pago_minimo and pago_maximo:
            if not CreditoService.validate_payment_range(pago_minimo, pago_maximo):
                return (
                    False,
                    'El pago mínimo debe ser menor o igual al pago máximo'
                )
        
        return (True, None)
    
    @staticmethod
    def get_credit_statistics(banco_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Calcula estadísticas de créditos.
        
        Args:
            banco_id: ID del banco (opcional) para filtrar por banco
            
        Returns:
            Dict con estadísticas
        """
        queryset = Credito.objects.all()
        
        if banco_id:
            queryset = queryset.filter(banco_id=banco_id)
        
        total_creditos = queryset.count()
        total_monto_minimo = queryset.aggregate(
            total=models.Sum('pago_minimo')
        )['total'] or Decimal('0.00')
        
        total_monto_maximo = queryset.aggregate(
            total=models.Sum('pago_maximo')
        )['total'] or Decimal('0.00')
        
        creditos_por_tipo = {}
        for tipo in TipoCredito:
            creditos_por_tipo[tipo.label] = queryset.filter(tipo_credito=tipo).count()
        
        return {
            'total_creditos': total_creditos,
            'total_monto_minimo': float(total_monto_minimo),
            'total_monto_maximo': float(total_monto_maximo),
            'creditos_por_tipo': creditos_por_tipo
        }
