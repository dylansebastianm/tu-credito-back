"""
URL configuration for bancos app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.bancos.views import BancoViewSet

router = DefaultRouter()
router.register(r'', BancoViewSet, basename='banco')

urlpatterns = [
    path('', include(router.urls)),
]
