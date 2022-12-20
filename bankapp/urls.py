"""bankapp URL Configuration"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_nested import routers

from wallets.views import WalletViewSet, TransactionViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallets')
router.register(r'user', UserViewSet, basename='user')

wallet_router = routers.NestedDefaultRouter(router, r'wallets', lookup='wallet')
wallet_router.register(r'transactions', TransactionViewSet, basename='transactions')
# router.register(r'wallets/transaction', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(wallet_router.urls)),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('wallets/transaction/', TransactionViewSet.as_view())
]
