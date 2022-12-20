"""Views config"""
import string
import random

from django.db.transaction import atomic
from django.db.models import Q

from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wallets.models import Wallet, User, Transaction
from wallets.serializers import WalletSerializer, UserSerializer, TransactionSerializer


def name() -> str:
    """Generate wallet name"""
    letters = string.ascii_uppercase + string.digits
    res = ''.join(random.choice(letters) for _ in range(8))
    return res


class WalletViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    """Wallet ViewSet"""
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "name"

    def create(self, request: Request) -> Response:
        """Post wallet"""
        post_data = {'type': request.data['type'], 'currency': request.data['currency']}
        #        logging.info(post_data)
        if post_data['currency'] == 'RUB':
            balance = 100.00
        else:
            balance = 3.00
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, name=name(), balance=balance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    """User ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionViewSet(GenericViewSet,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin):
    """Transaction ViewSet"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, wallet_name=None) -> Response:
        """Post transaction"""
        post_data = {
            'sender': request.data['sender'],
            'receiver': request.data['receiver'],
            'transfer_amount': request.data['transfer_amount'],
        }
        sender = Wallet.objects.get(pk=request.data['sender'])
        receiver = Wallet.objects.get(pk=request.data['receiver'])
        if sender.currency != receiver.currency:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if sender.owner == receiver.owner:
            commission = 0
        else:
            commission = post_data['transfer_amount'] * 0.1
        if sender.balance < (float(post_data['transfer_amount']) + commission):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        with atomic():
            sender.balance = float(sender.balance) - float(post_data['transfer_amount'])
            receiver.balance = float(receiver.balance) + float(post_data['transfer_amount'])
            sender.save()
            receiver.save()
            _status = "PAID"
            serializer = self.get_serializer(data=post_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(status=_status)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request: Request, wallet_name=None) -> Response:
        """Get all transaction for wallet_name"""
        queryset = Transaction.objects.filter(Q(sender__name=wallet_name) | Q(receiver__name=wallet_name))
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, wallet_name=None, pk=None) -> Response:
        """Get a detail transaction"""
        queryset = Transaction.objects.filter(Q(sender__name=wallet_name) | Q(receiver__name=wallet_name))
        transaction = get_object_or_404(queryset, pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
