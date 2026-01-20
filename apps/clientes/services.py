"""
Services layer for Cliente business logic.
Separates business logic from views and models for better architecture.
"""
from typing import Optional, Dict, Any
from django.db import transaction
from apps.clientes.models import Cliente


class ClienteService:
    """
    Service class for Cliente business logic operations.
    """
    
    @staticmethod
    def can_delete_cliente(cliente: Cliente) -> tuple[bool, Optional[str]]:
        """
        Verifica si un cliente puede ser eliminado.
        
        Args:
            cliente: Instancia del Cliente a verificar
            
        Returns:
            Tuple (can_delete: bool, error_message: Optional[str])
        """
        if cliente.creditos.exists():
            creditos_count = cliente.creditos.count()
            return (
                False,
                f'No se puede eliminar el cliente porque tiene {creditos_count} crédito(s) asociado(s)'
            )
        return (True, None)
    
    @staticmethod
    def delete_cliente_if_safe(cliente: Cliente) -> Dict[str, Any]:
        """
        Elimina un cliente solo si es seguro hacerlo.
        
        Args:
            cliente: Instancia del Cliente a eliminar
            
        Returns:
            Dict con el resultado de la operación
        """
        can_delete, error_message = ClienteService.can_delete_cliente(cliente)
        
        if not can_delete:
            return {
                'success': False,
                'error': True,
                'message': error_message,
                'details': {
                    'creditos_count': cliente.creditos.count()
                }
            }
        
        with transaction.atomic():
            cliente_id = cliente.id
            cliente.delete()
        
        return {
            'success': True,
            'message': f'Cliente {cliente_id} eliminado correctamente'
        }
    
    @staticmethod
    def get_cliente_with_creditos(cliente_id: int) -> Optional[Cliente]:
        """
        Obtiene un cliente con sus créditos relacionados.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Cliente instance o None si no existe
        """
        try:
            return Cliente.objects.select_related('banco').prefetch_related('creditos').get(id=cliente_id)
        except Cliente.DoesNotExist:
            return None
