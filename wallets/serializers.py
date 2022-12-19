from rest_framework import serializers
from wallets.models import Wallet, User, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ("modified_on", "created_on", 'name', 'balance', 'owner')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'username', 'email']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        extra_kwargs = {
            'sender': {'write_only': True},
            'receiver': {'write_only': True},
            'transfer_amount': {'write_only': True},
        }
