"""
Tests for health check endpoint.
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestHealthCheck:
    """Tests para el endpoint de health check."""
    
    def test_health_check_sin_autenticacion(self, api_client):
        """Test que health check no requiere autenticación."""
        url = reverse('health')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'healthy'
        assert response.data['database'] == 'connected'
