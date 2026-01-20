"""
URL configuration for creditos app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.creditos.views import CreditoViewSet

router = DefaultRouter()
router.register(r'', CreditoViewSet, basename='credito')

urlpatterns = [
    path('', include(router.urls)),
]
