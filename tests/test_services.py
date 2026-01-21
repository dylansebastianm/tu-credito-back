"""
Tests for Service Layer - Bloque C Senior
Tests para validar la lógica de negocio en los servicios.
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from apps.bancos.models import Banco, TipoBanco
from apps.bancos.services import BancoService
from apps.clientes.models import Cliente, TipoPersona
from apps.clientes.services import ClienteService
from apps.creditos.models import Credito, TipoCredito
from apps.creditos.services import CreditoService


@pytest.mark.django_db
class TestBancoService:
    """Tests para BancoService."""
    
    def test_can_delete_banco_sin_creditos(self):
        """Test que un banco sin créditos puede ser eliminado."""
        banco = Banco.objects.create(
            nombre='Banco Test',
            tipo=TipoBanco.PRIVADO
        )
        
        can_delete, error_message = BancoService.can_delete_banco(banco)
        
        assert can_delete is True
        assert error_message is None
    
    def test_can_delete_banco_con_creditos(self):
        """Test que un banco con créditos NO puede ser eliminado."""
        banco = Banco.objects.create(
            nombre='Banco Test',
            tipo=TipoBanco.PRIVADO
        )
        
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Cliente Test',
            fecha_nacimiento=fecha_nac,
            email='cliente@test.com',
            tipo_persona=TipoPersona.NATURAL
        )
        
        Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Crédito test',
            monto=Decimal('10000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('2000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        can_delete, error_message = BancoService.can_delete_banco(banco)
        
        assert can_delete is False
        assert error_message is not None
        assert 'crédito' in error_message.lower()
    
    def test_delete_banco_if_safe_success(self):
        """Test eliminar banco cuando es seguro."""
        banco = Banco.objects.create(
            nombre='Banco Test',
            tipo=TipoBanco.PRIVADO
        )
        banco_id = banco.id
        
        result = BancoService.delete_banco_if_safe(banco)
        
        assert result['success'] is True
        assert 'eliminado' in result['message'].lower()
        assert not Banco.objects.filter(id=banco_id).exists()
    
    def test_delete_banco_if_safe_failure(self):
        """Test que no se elimina banco cuando tiene créditos."""
        banco = Banco.objects.create(
            nombre='Banco Test',
            tipo=TipoBanco.PRIVADO
        )
        
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Cliente Test',
            fecha_nacimiento=fecha_nac,
            email='cliente@test.com',
            tipo_persona=TipoPersona.NATURAL
        )
        
        Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Crédito test',
            monto=Decimal('10000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('2000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        result = BancoService.delete_banco_if_safe(banco)
        
        assert result['success'] is False
        assert result['error'] is True
        assert 'creditos_count' in result['details']
        assert Banco.objects.filter(id=banco.id).exists()  # No se eliminó


@pytest.mark.django_db
class TestClienteService:
    """Tests para ClienteService."""
    
    def test_can_delete_cliente_sin_creditos(self):
        """Test que un cliente sin créditos puede ser eliminado."""
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Cliente Test',
            fecha_nacimiento=fecha_nac,
            email='cliente@test.com',
            tipo_persona=TipoPersona.NATURAL
        )
        
        can_delete, error_message = ClienteService.can_delete_cliente(cliente)
        
        assert can_delete is True
        assert error_message is None
    
    def test_can_delete_cliente_con_creditos(self):
        """Test que un cliente con créditos NO puede ser eliminado."""
        banco = Banco.objects.create(
            nombre='Banco Test',
            tipo=TipoBanco.PRIVADO
        )
        
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Cliente Test',
            fecha_nacimiento=fecha_nac,
            email='cliente@test.com',
            tipo_persona=TipoPersona.NATURAL
        )
        
        Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Crédito test',
            monto=Decimal('10000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('2000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        can_delete, error_message = ClienteService.can_delete_cliente(cliente)
        
        assert can_delete is False
        assert error_message is not None
        assert 'crédito' in error_message.lower()
    
    def test_delete_cliente_if_safe_success(self):
        """Test eliminar cliente cuando es seguro."""
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Cliente Test',
            fecha_nacimiento=fecha_nac,
            email='cliente@test.com',
            tipo_persona=TipoPersona.NATURAL
        )
        cliente_id = cliente.id
        
        result = ClienteService.delete_cliente_if_safe(cliente)
        
        assert result['success'] is True
        assert 'eliminado' in result['message'].lower()
        assert not Cliente.objects.filter(id=cliente_id).exists()
    
    def test_delete_cliente_if_safe_failure(self):
        """Test que no se elimina cliente cuando tiene créditos."""
        banco = Banco.objects.create(
            nombre='Banco Test',
            tipo=TipoBanco.PRIVADO
        )
        
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Cliente Test',
            fecha_nacimiento=fecha_nac,
            email='cliente@test.com',
            tipo_persona=TipoPersona.NATURAL
        )
        
        Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Crédito test',
            monto=Decimal('10000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('2000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        result = ClienteService.delete_cliente_if_safe(cliente)
        
        assert result['success'] is False
        assert result['error'] is True
        assert 'creditos_count' in result['details']
        assert Cliente.objects.filter(id=cliente.id).exists()  # No se eliminó
    
    def test_get_cliente_with_creditos(self):
        """Test obtener cliente con créditos relacionados."""
        banco = Banco.objects.create(
            nombre='Banco Test',
            tipo=TipoBanco.PRIVADO
        )
        
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Cliente Test',
            fecha_nacimiento=fecha_nac,
            email='cliente@test.com',
            tipo_persona=TipoPersona.NATURAL,
            banco=banco
        )
        
        Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Crédito test',
            monto=Decimal('10000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('2000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        result = ClienteService.get_cliente_with_creditos(cliente.id)
        
        assert result is not None
        assert result.id == cliente.id
        # Verificar que tiene créditos relacionados (prefetch_related)
        assert hasattr(result, 'creditos')
    
    def test_get_cliente_with_creditos_not_found(self):
        """Test obtener cliente inexistente."""
        result = ClienteService.get_cliente_with_creditos(99999)
        
        assert result is None


@pytest.mark.django_db
class TestCreditoService:
    """Tests para CreditoService."""
    
    def test_validate_payment_range_valid(self):
        """Test validar rango de pago válido."""
        pago_minimo = Decimal('1000.00')
        pago_maximo = Decimal('2000.00')
        
        result = CreditoService.validate_payment_range(pago_minimo, pago_maximo)
        
        assert result is True
    
    def test_validate_payment_range_equal(self):
        """Test validar rango de pago cuando son iguales."""
        pago_minimo = Decimal('1000.00')
        pago_maximo = Decimal('1000.00')
        
        result = CreditoService.validate_payment_range(pago_minimo, pago_maximo)
        
        assert result is True
    
    def test_validate_payment_range_invalid(self):
        """Test validar rango de pago inválido."""
        pago_minimo = Decimal('2000.00')
        pago_maximo = Decimal('1000.00')
        
        result = CreditoService.validate_payment_range(pago_minimo, pago_maximo)
        
        assert result is False
    
    def test_validate_credit_data_valid(self):
        """Test validar datos de crédito válidos."""
        data = {
            'pago_minimo': Decimal('1000.00'),
            'pago_maximo': Decimal('2000.00'),
        }
        
        is_valid, error_message = CreditoService.validate_credit_data(data)
        
        assert is_valid is True
        assert error_message is None
    
    def test_validate_credit_data_invalid_range(self):
        """Test validar datos de crédito con rango inválido."""
        data = {
            'pago_minimo': Decimal('2000.00'),
            'pago_maximo': Decimal('1000.00'),
        }
        
        is_valid, error_message = CreditoService.validate_credit_data(data)
        
        assert is_valid is False
        assert error_message is not None
        assert 'pago mínimo' in error_message.lower()
    
    def test_validate_credit_data_missing_fields(self):
        """Test validar datos de crédito sin campos de pago."""
        data = {
            'descripcion': 'Test crédito',
        }
        
        is_valid, error_message = CreditoService.validate_credit_data(data)
        
        assert is_valid is True  # Sin campos de pago, no hay error
        assert error_message is None
    
    def test_get_credit_statistics_all(self):
        """Test obtener estadísticas de todos los créditos."""
        banco = Banco.objects.create(
            nombre='Banco Test',
            tipo=TipoBanco.PRIVADO
        )
        
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente1 = Cliente.objects.create(
            nombre_completo='Cliente 1',
            fecha_nacimiento=fecha_nac,
            email='cliente1@test.com',
            tipo_persona=TipoPersona.NATURAL
        )
        
        cliente2 = Cliente.objects.create(
            nombre_completo='Cliente 2',
            fecha_nacimiento=fecha_nac,
            email='cliente2@test.com',
            tipo_persona=TipoPersona.NATURAL
        )
        
        Credito.objects.create(
            cliente=cliente1,
            banco=banco,
            descripcion='Crédito 1',
            monto=Decimal('10000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('2000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        Credito.objects.create(
            cliente=cliente2,
            banco=banco,
            descripcion='Crédito 2',
            monto=Decimal('20000.00'),
            pago_minimo=Decimal('2000.00'),
            pago_maximo=Decimal('3000.00'),
            plazo_meses=24,
            tipo_credito=TipoCredito.AUTOMOTRIZ
        )
        
        stats = CreditoService.get_credit_statistics()
        
        assert stats['total_creditos'] == 2
        assert stats['total_monto_minimo'] == 3000.0
        assert stats['total_monto_maximo'] == 5000.0
        assert 'creditos_por_tipo' in stats
    
    def test_get_credit_statistics_by_banco(self):
        """Test obtener estadísticas filtradas por banco."""
        banco1 = Banco.objects.create(
            nombre='Banco 1',
            tipo=TipoBanco.PRIVADO
        )
        
        banco2 = Banco.objects.create(
            nombre='Banco 2',
            tipo=TipoBanco.GOBIERNO
        )
        
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Cliente Test',
            fecha_nacimiento=fecha_nac,
            email='cliente@test.com',
            tipo_persona=TipoPersona.NATURAL
        )
        
        Credito.objects.create(
            cliente=cliente,
            banco=banco1,
            descripcion='Crédito 1',
            monto=Decimal('10000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('2000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        Credito.objects.create(
            cliente=cliente,
            banco=banco2,
            descripcion='Crédito 2',
            monto=Decimal('20000.00'),
            pago_minimo=Decimal('2000.00'),
            pago_maximo=Decimal('3000.00'),
            plazo_meses=24,
            tipo_credito=TipoCredito.AUTOMOTRIZ
        )
        
        stats = CreditoService.get_credit_statistics(banco_id=banco1.id)
        
        assert stats['total_creditos'] == 1
        assert stats['total_monto_minimo'] == 1000.0
        assert stats['total_monto_maximo'] == 2000.0
