"""
Tests for Banco model and API.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from apps.bancos.models import Banco, TipoBanco


@pytest.mark.django_db
class TestBancoModel:
    """Tests para el modelo Banco."""
    
    def test_crear_banco(self):
        """Test crear un banco válido."""
        banco = Banco.objects.create(
            nombre='Banco de Prueba',
            tipo=TipoBanco.PRIVADO,
            direccion='Calle 123'
        )
        assert banco.id is not None
        assert banco.nombre == 'Banco de Prueba'
        assert banco.tipo == TipoBanco.PRIVADO
    
    def test_banco_str(self):
        """Test representación string del banco."""
        banco = Banco.objects.create(
            nombre='Banco Test',
            tipo=TipoBanco.GOBIERNO
        )
        assert 'Banco Test' in str(banco)
        assert 'Gobierno' in str(banco)


@pytest.mark.django_db
class TestBancoAPI:
    """Tests para la API de Bancos."""
    
    def test_listar_bancos(self, authenticated_client):
        """Test listar bancos."""
        Banco.objects.create(nombre='Banco 1', tipo=TipoBanco.PRIVADO)
        Banco.objects.create(nombre='Banco 2', tipo=TipoBanco.GOBIERNO)
        
        url = reverse('banco-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
    
    def test_crear_banco(self, authenticated_client):
        """Test crear banco vía API."""
        url = reverse('banco-list')
        data = {
            'nombre': 'Nuevo Banco',
            'tipo': TipoBanco.PRIVADO,
            'direccion': 'Calle 456'
        }
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Banco.objects.filter(nombre='Nuevo Banco').exists()
    
    def test_crear_banco_sin_autenticacion(self, api_client):
        """Test que requiere autenticación."""
        url = reverse('banco-list')
        data = {'nombre': 'Banco', 'tipo': TipoBanco.PRIVADO}
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_validar_nombre_requerido(self, authenticated_client):
        """Test validar que nombre es requerido."""
        url = reverse('banco-list')
        data = {'tipo': TipoBanco.PRIVADO}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'nombre' in response.data['details']
    
    def test_validar_tipo_requerido(self, authenticated_client):
        """Test validar que tipo es requerido."""
        url = reverse('banco-list')
        data = {'nombre': 'Banco Test'}
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'tipo' in response.data['details']
    
    def test_filtrar_por_tipo(self, authenticated_client):
        """Test filtrar bancos por tipo."""
        Banco.objects.create(nombre='Banco Privado', tipo=TipoBanco.PRIVADO)
        Banco.objects.create(nombre='Banco Gobierno', tipo=TipoBanco.GOBIERNO)
        
        url = reverse('banco-list')
        response = authenticated_client.get(url, {'tipo': TipoBanco.PRIVADO})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['tipo'] == TipoBanco.PRIVADO
