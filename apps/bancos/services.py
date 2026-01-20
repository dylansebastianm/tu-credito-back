"""
Services layer for Banco business logic.
Separates business logic from views and models for better architecture.
"""
from typing import Optional, Dict, Any
from django.db import transaction
from apps.bancos.models import Banco


class BancoService:
    """
    Service class for Banco business logic operations.
    """
    
    @staticmethod
    def can_delete_banco(banco: Banco) -> tuple[bool, Optional[str]]:
        """
        Verifica si un banco puede ser eliminado.
        
        Args:
            banco: Instancia del Banco a verificar
            
        Returns:
            Tuple (can_delete: bool, error_message: Optional[str])
        """
        if banco.creditos.exists():
            creditos_count = banco.creditos.count()
            return (
                False,
                f'No se puede eliminar el banco porque tiene {creditos_count} crédito(s) asociado(s)'
            )
        return (True, None)
    
    @staticmethod
    def delete_banco_if_safe(banco: Banco) -> Dict[str, Any]:
        """
        Elimina un banco solo si es seguro hacerlo.
        
        Args:
            banco: Instancia del Banco a eliminar
            
        Returns:
            Dict con el resultado de la operación
        """
        can_delete, error_message = BancoService.can_delete_banco(banco)
        
        if not can_delete:
            return {
                'success': False,
                'error': True,
                'message': error_message,
                'details': {
                    'creditos_count': banco.creditos.count()
                }
            }
        
        with transaction.atomic():
            banco_id = banco.id
            banco.delete()
        
        return {
            'success': True,
            'message': f'Banco {banco_id} eliminado correctamente'
        }
