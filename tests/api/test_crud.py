import pytest
from rest_framework.test import APIClient
from wallets.models import User


@pytest.fixture()
def autorizated_client():
    client = APIClient()
    obj = User.objects.create(username="test2",
                              password="test2",
                              email="test2@test2.com")
    obj.save()
    client.force_authenticate(user=obj)
    return client


@pytest.fixture()
def created_wallet(autorizated_client):
    payload = {
        "type": "VISA",
        "currency": "USD"
    }
    response = autorizated_client.post("/wallets/", payload)
    return response


@pytest.mark.django_db
def test_create_wallet(autorizated_client):
    """Create wallet test"""
    payload = {
        "type": "VISA",
        "currency": "USD"
    }
    response = autorizated_client.post("/wallets/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_wallets(autorizated_client):
    """Test get all wallets"""
    response = autorizated_client.get("/wallets/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_wallet(autorizated_client, created_wallet):
    """Test get a wallet"""
    response = autorizated_client.get(f"/wallets/{created_wallet.data['name']}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_wallet(autorizated_client, created_wallet):
    """Test delete a wallet"""
    response = autorizated_client.delete(f"/wallets/{created_wallet.data['name']}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_create_transaction(autorizated_client, created_wallet):
    """Test crete a transaction"""
    payload = {
        "type": "VISA",
        "currency": "USD"
    }
    sender = autorizated_client.post("/wallets/", payload)
    payload = {
        "receiver": created_wallet.data['id'],
        "sender": sender.data['id'],
        "transfer_amount": 1.00,
    }
    response = autorizated_client.post(f"/wallets/{created_wallet.data['name']}/transactions/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_wrong_currency_transaction(autorizated_client, created_wallet):
    """Test crete a transaction"""
    payload = {
        "type": "VISA",
        "currency": "RUB"
    }
    sender = autorizated_client.post("/wallets/", payload)
    payload = {
        "receiver": created_wallet.data['id'],
        "sender": sender.data['id'],
        "transfer_amount": 1.00,
    }
    response = autorizated_client.post(f"/wallets/{created_wallet.data['name']}/transactions/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_wrong_amount_transaction(autorizated_client, created_wallet):
    """Test crete a transaction"""
    payload = {
        "type": "VISA",
        "currency": "USD"
    }
    sender = autorizated_client.post("/wallets/", payload)
    payload = {
        "receiver": created_wallet.data['id'],
        "sender": sender.data['id'],
        "transfer_amount": 999.00,
    }
    response = autorizated_client.post(f"/wallets/{created_wallet.data['name']}/transactions/", payload)
    assert response.status_code == 400
