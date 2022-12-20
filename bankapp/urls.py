"""bankapp URL Configuration"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from wallets.views import WalletViewSet, TransactionViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallet')
router.register(r'user', UserViewSet, basename='user')
router.register(r'transaction', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('wallets/transaction/', TransactionViewSet.as_view())
]
