"""Serializers"""
from rest_framework import serializers
from wallets.models import Wallet, User, Transaction


class WalletSerializer(serializers.ModelSerializer):
    """Wallet Serializer"""
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ("modified_on", "created_on", 'name', 'balance', 'owner')


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    class Meta:
        model = User
        fields = ['password', 'username', 'email']


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction Serializer"""
    parent_lookup_kwargs = {
        'wallet_pk': 'wallet__pk',
    }

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ("status", "commission")
