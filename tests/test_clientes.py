"""
Tests for Cliente model and API.
"""
import pytest
from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from apps.clientes.models import Cliente, TipoPersona
from apps.bancos.models import Banco, TipoBanco


@pytest.mark.django_db
class TestClienteModel:
    """Tests para el modelo Cliente."""
    
    def test_crear_cliente(self):
        """Test crear un cliente válido."""
        fecha_nacimiento = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Juan Pérez',
            fecha_nacimiento=fecha_nacimiento,
            edad=30,
            email='juan@example.com',
            tipo_persona=TipoPersona.NATURAL
        )
        assert cliente.id is not None
        assert cliente.email == 'juan@example.com'
        # La edad se calcula automáticamente (puede variar según el día)
        assert cliente.edad >= 29 and cliente.edad <= 31
    
    def test_calcular_edad_automaticamente(self):
        """Test que la edad se calcula automáticamente."""
        fecha_nacimiento = date.today() - timedelta(days=365 * 25)
        cliente = Cliente(
            nombre_completo='María García',
            fecha_nacimiento=fecha_nacimiento,
            email='maria@example.com',
            tipo_persona=TipoPersona.NATURAL
        )
        # No establecer edad explícitamente
        cliente.save()
        
        # La edad debe calcularse automáticamente
        assert cliente.edad > 0
        assert cliente.edad <= 99
    
    def test_validar_edad_coherente(self):
        """Test validar que edad se calcula automáticamente desde fecha_nacimiento."""
        fecha_nacimiento = date.today() - timedelta(days=365 * 30)
        cliente = Cliente(
            nombre_completo='Test User',
            fecha_nacimiento=fecha_nacimiento,
            email='test@example.com',
            tipo_persona=TipoPersona.NATURAL
        )
        # La edad se calcula automáticamente en save(), no se valida en clean()
        cliente.save()
        # Verificar que la edad calculada es aproximadamente 30
        assert cliente.edad >= 29 and cliente.edad <= 31


@pytest.mark.django_db
class TestClienteAPI:
    """Tests para la API de Clientes."""
    
    def test_listar_clientes(self, authenticated_client):
        """Test listar clientes."""
        fecha_nac = date.today() - timedelta(days=365 * 25)
        Cliente.objects.create(
            nombre_completo='Cliente 1',
            fecha_nacimiento=fecha_nac,
            edad=25,
            email='cliente1@example.com'
        )
        
        url = reverse('cliente-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
    
    def test_crear_cliente(self, authenticated_client):
        """Test crear cliente vía API."""
        fecha_nac = date.today() - timedelta(days=365 * 30)
        url = reverse('cliente-list')
        data = {
            'nombre_completo': 'Nuevo Cliente',
            'fecha_nacimiento': fecha_nac.isoformat(),
            'email': 'nuevo@example.com',
            'tipo_persona': TipoPersona.NATURAL
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Cliente.objects.filter(email='nuevo@example.com').exists()
        # Verificar que la edad se calculó automáticamente
        cliente = Cliente.objects.get(email='nuevo@example.com')
        assert cliente.edad > 0
    
    def test_validar_email_requerido(self, authenticated_client):
        """Test validar que email es requerido."""
        fecha_nac = date.today() - timedelta(days=365 * 25)
        url = reverse('cliente-list')
        data = {
            'nombre_completo': 'Test',
            'fecha_nacimiento': fecha_nac.isoformat()
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data['details']
    
    def test_validar_email_unico(self, authenticated_client):
        """Test validar que email es único."""
        fecha_nac = date.today() - timedelta(days=365 * 25)
        Cliente.objects.create(
            nombre_completo='Cliente Existente',
            fecha_nacimiento=fecha_nac,
            edad=25,
            email='duplicado@example.com'
        )
        
        url = reverse('cliente-list')
        data = {
            'nombre_completo': 'Otro Cliente',
            'fecha_nacimiento': fecha_nac.isoformat(),
            'email': 'duplicado@example.com',
            'tipo_persona': TipoPersona.NATURAL
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_no_eliminar_cliente_con_creditos(self, authenticated_client):
        """Test que no se puede eliminar cliente con créditos."""
        from apps.creditos.models import Credito, TipoCredito
        
        banco = Banco.objects.create(nombre='Banco Test', tipo=TipoBanco.PRIVADO)
        fecha_nac = date.today() - timedelta(days=365 * 30)
        cliente = Cliente.objects.create(
            nombre_completo='Cliente con Crédito',
            fecha_nacimiento=fecha_nac,
            edad=30,
            email='concredito@example.com'
        )
        
        from decimal import Decimal
        
        Credito.objects.create(
            cliente=cliente,
            banco=banco,
            descripcion='Test',
            monto=Decimal('50000.00'),
            pago_minimo=Decimal('1000.00'),
            pago_maximo=Decimal('5000.00'),
            plazo_meses=12,
            tipo_credito=TipoCredito.COMERCIAL
        )
        
        url = reverse('cliente-detail', kwargs={'pk': cliente.id})
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'crédito' in response.data['message'].lower()
