"""
Tests for Credito model and API.
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from apps.creditos.models import Credito, TipoCredito
from apps.clientes.models import Cliente, TipoPersona
from apps.bancos.models import Banco, TipoBanco


@pytest.fixture
def banco():
    """Fixture para crear un banco."""
    return Banco.objects.create(
        nombre='Banco de Prueba',
        tipo=TipoBanco.PRIVADO
    )


@pytest.fixture
def cliente():
    """Fixture para crear un cliente."""
    fecha_nac = date.today() - timedelta(days=365 * 30)
    return Cliente.objects.create(
        nombre_completo='Cliente de Prueba',
        fecha_nacimiento=fecha_nac,
        edad=30,
        email='cliente@example.com',
        tipo_persona=TipoPersona.NATURAL
    )


@pytest.mark.django_db
class TestCreditoModel:
    """Tests para el modelo Credito."""
    
    def test_crear_credito(self, cliente, banco):
        """Test crear un crédito válido."""
        credito = Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Crédito de prueba',
            monto=Decimal('50000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('5000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        assert credito.id is not None
        assert credito.pago_minimo == Decimal('1000.00')
        assert credito.pago_maximo == Decimal('5000.00')
    
    def test_validar_pago_minimo_menor_igual_maximo(self, cliente, banco):
        """Test validar que pago_minimo <= pago_maximo."""
        credito = Credito(
            cliente=cliente,
            banco=banco,
            descripcion='Test',
            monto=Decimal('50000.00'),
            pago_minimo=Decimal('5000.00'),
            pago_maximo=Decimal('1000.00'),  # Incorrecto
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        with pytest.raises(Exception):  # ValidationError
            credito.full_clean()


@pytest.mark.django_db
class TestCreditoAPI:
    """Tests para la API de Créditos."""
    
    def test_listar_creditos(self, authenticated_client, cliente, banco):
        """Test listar créditos."""
        Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Crédito 1',
            monto=Decimal('50000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('5000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        url = reverse('credito-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
    
    def test_crear_credito(self, authenticated_client, cliente, banco):
        """Test crear crédito vía API."""
        url = reverse('credito-list')
        data = {
            'cliente': cliente.id,
            'banco': banco.id,
            'descripcion': 'Nuevo Crédito',
            'monto': '50000.00',
            'pago_minimo': '1000.00',
            'pago_maximo': '5000.00',
            'plazo_meses': 24,
            'tipo_credito': TipoCredito.HIPOTECARIO
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Credito.objects.filter(descripcion='Nuevo Crédito').exists()
    
    def test_validar_pago_minimo_requerido(self, authenticated_client, cliente, banco):
        """Test validar que pago_minimo es requerido."""
        url = reverse('credito-list')
        data = {
            'cliente': cliente.id,
            'banco': banco.id,
            'descripcion': 'Test',
            'pago_maximo': '5000.00',
            'plazo_meses': 12,
            'tipo_credito': TipoCredito.COMERCIAL
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'pago_minimo' in response.data['details']
    
    def test_validar_pago_maximo_mayor_igual_minimo(self, authenticated_client, cliente, banco):
        """Test validar que pago_maximo >= pago_minimo."""
        url = reverse('credito-list')
        data = {
            'cliente': cliente.id,
            'banco': banco.id,
            'descripcion': 'Test',
            'monto': '50000.00',
            'pago_minimo': '5000.00',
            'pago_maximo': '1000.00',  # Incorrecto
            'plazo_meses': 12,
            'tipo_credito': TipoCredito.COMERCIAL
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'pago_maximo' in response.data['details']
    
    def test_filtrar_por_tipo_credito(self, authenticated_client, cliente, banco):
        """Test filtrar créditos por tipo."""
        Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Crédito Comercial',
            monto=Decimal('50000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('5000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Crédito Hipotecario',
            monto=Decimal('200000.00'),
            pago_minimo=Decimal('2000.00'),
            pago_maximo=Decimal('10000.00'),
            plazo_meses=36,
            tipo_credito=TipoCredito.HIPOTECARIO
        )
        
        url = reverse('credito-list')
        response = authenticated_client.get(url, {'tipo_credito': TipoCredito.COMERCIAL})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['tipo_credito'] == TipoCredito.COMERCIAL
