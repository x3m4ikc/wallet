import string
import random

from django.shortcuts import render
import logging
from rest_framework.request import Request
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wallets.models import Wallet, User, Transaction
from wallets.serializers import WalletSerializer, UserSerializer, TransactionSerializer

# logging.basicConfig(filename="log.log", level=logging.INFO, encoding='utf-8')


def name():
    letters = string.ascii_uppercase + string.digits
    res = ''.join(random.choice(letters) for _ in range(8))
#     res = "111111"
    return res


class WalletViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request):
        post_data = {'type': request.data['type'], 'currency': request.data['currency']}
#        logging.info(post_data)
        if post_data['currency'] == 'RUB':
            balance = 100.00
        else:
            balance = 3.00
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, name=name() ,balance=balance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
from django.shortcuts import render

# Create your views here.
