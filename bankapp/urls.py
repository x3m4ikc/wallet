"""bankapp URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from wallets.views import WalletViewSet, TransactionViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallet')
router.register(r'user', UserViewSet, basename='user')
router.register(r'wallets/transaction', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('drf-auth/', include('rest_framework.urls')),
#    path('wallets/<name:slug>', WalletViewSet)
]
