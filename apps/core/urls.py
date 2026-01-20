"""
URL configuration for core app.
"""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from apps.core.views import (
    CurrentUserView,
    RegisterView,
    EmailTokenObtainPairView
)

urlpatterns = [
    path('auth/token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/me/', CurrentUserView.as_view(), name='current_user'),
    path('bancos/', include('apps.bancos.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('creditos/', include('apps.creditos.urls')),
]
