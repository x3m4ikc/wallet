import pytest
from rest_framework.test import APIClient
from wallets.models import Wallet

client = APIClient()


@pytest.mark.django_db
def test_create_wallet():
    """Create wallet test"""
    payload = {
        "name": "admin",
        "password": "admin"
    }
    response = client.post("/drf-auth/login/?next=/auth/users/", payload)
    payload = {
        "type": "VISA",
        "currency": "USD"
    }
    response = client.post("/wallets/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_wallets():
    """Test get all wallets"""
    response = client.get("/wallets/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_wallet():
    """Test get a wallet"""
    random_wallet = Wallet.objects.all()[0].name
    response = client.get(f"/wallets/{random_wallet}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_wallet():
    """Test delete a wallet"""
    random_wallet = Wallet.objects.all()[-1].name
    response = client.delete(f"/wallets/{random_wallet}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_transaction():
    """Test crete a transaction"""
    receiver = Wallet.objects.all()[1].name
    sender = Wallet.objects.all()[2].name
    payload = {
        "receiver": receiver,
        "sender": sender,
        "transfer_amount": 10.00,
    }
    response = client.post("/wallets/transaction/", payload)
    assert response.status_code == 201
