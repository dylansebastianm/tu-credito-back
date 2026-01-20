"""
URL configuration for core app.
"""
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bancos/', include('apps.bancos.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('creditos/', include('apps.creditos.urls')),
]
