import string
import random

from django.db import transaction
from django.shortcuts import render
import logging
from rest_framework.request import Request
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wallets.models import Wallet, User, Transaction
from wallets.serializers import WalletSerializer, UserSerializer, TransactionSerializer

# logging.basicConfig(filename="log.log", level=logging.INFO, encoding='utf-8')


def name():
    letters = string.ascii_uppercase + string.digits
    res = ''.join(random.choice(letters) for _ in range(8))
    return res


class WalletViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "name"

    def create(self, request: Request):
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
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionViewSet(GenericViewSet,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request: Request):
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
        with transaction.atomic():
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
