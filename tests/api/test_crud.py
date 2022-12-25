import pytest
from rest_framework.test import APIClient
from wallets.models import User


@pytest.fixture()
def authorized_client():
    client = APIClient()
    obj = User.objects.create(username="test2",
                              password="test2",
                              email="test2@test2.com")
    obj.save()
    client.force_authenticate(user=obj)
    return client


@pytest.fixture()
def created_wallet(authorized_client):
    payload = {
        "type": "VISA",
        "currency": "USD"
    }
    response = authorized_client.post("/wallets/", payload)
    return response


@pytest.mark.django_db
@pytest.mark.parametrize("payload, result",
                         [({"type": "VISA", "currency": "USD"}, 201),
                          ({"type": "MASTERCARD", "currency": "USD"}, 201),
                          ({"type": "VISA", "currency": "EUR"}, 201),
                          ({"type": "VISA", "currency": "RUB"}, 201)])
def test_create_wallet(payload, result, authorized_client):
    """Create wallet test"""
    response = authorized_client.post("/wallets/", payload)
    assert response.status_code == result


@pytest.mark.django_db
def test_get_wallets(authorized_client):
    """Test get all wallets"""
    response = authorized_client.get("/wallets/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_wallet(authorized_client, created_wallet):
    """Test get a wallet"""
    response = authorized_client.get(f"/wallets/{created_wallet.data['name']}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_wallet(authorized_client, created_wallet):
    """Test delete a wallet"""
    response = authorized_client.delete(f"/wallets/{created_wallet.data['name']}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_create_transaction(authorized_client, created_wallet):
    """Test crete a transaction"""
    payload = {
        "type": "VISA",
        "currency": "USD"
    }
    sender = authorized_client.post("/wallets/", payload)
    payload = {
        "receiver": created_wallet.data['id'],
        "sender": sender.data['id'],
        "transfer_amount": 1.00,
    }
    response = authorized_client.post(f"/wallets/{created_wallet.data['name']}/transactions/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_wrong_currency_transaction(authorized_client, created_wallet):
    """Test crete a transaction"""
    payload = {
        "type": "VISA",
        "currency": "RUB"
    }
    sender = authorized_client.post("/wallets/", payload)
    payload = {
        "receiver": created_wallet.data['id'],
        "sender": sender.data['id'],
        "transfer_amount": 1.00,
    }
    response = authorized_client.post(f"/wallets/{created_wallet.data['name']}/transactions/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_wrong_amount_transaction(authorized_client, created_wallet):
    """Test crete a transaction"""
    payload = {
        "type": "VISA",
        "currency": "USD"
    }
    sender = authorized_client.post("/wallets/", payload)
    payload = {
        "receiver": created_wallet.data['id'],
        "sender": sender.data['id'],
        "transfer_amount": 999.00,
    }
    response = authorized_client.post(f"/wallets/{created_wallet.data['name']}/transactions/", payload)
    assert response.status_code == 400
