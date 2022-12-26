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


# @pytest.mark.xfail
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


# @pytest.mark.xfail
@pytest.mark.django_db
def test_get_wallets(authorized_client):
    """Test get all wallets"""
    response = authorized_client.get("/wallets/")
    assert response.status_code == 200


# @pytest.mark.xfail
@pytest.mark.django_db
def test_get_wallet(authorized_client, created_wallet):
    """Test get a wallet"""
    response = authorized_client.get(f"/wallets/{created_wallet.data['name']}/")
    assert response.status_code == 200


# @pytest.mark.xfail
@pytest.mark.django_db
def test_delete_wallet(authorized_client, created_wallet):
    """Test delete a wallet"""
    response = authorized_client.delete(f"/wallets/{created_wallet.data['name']}/")
    assert response.status_code == 204


# @pytest.mark.xfail
@pytest.mark.django_db
@pytest.mark.parametrize("payload, transfer_amount, result",
                         [({"type": "VISA", "currency": "USD"}, 1.00, 201),  # ok create
                          ({"type": "VISA", "currency": "RUB"}, 1.00, 400),  # wrong currency
                          ({"type": "VISA", "currency": "USD"}, 999.00, 400)])  # wrong amount
def test_create_transaction(payload, transfer_amount, result, authorized_client, created_wallet):
    """Test crete a transaction"""
    sender = authorized_client.post("/wallets/", payload)
    post_data = {
        "receiver": created_wallet.data['id'],
        "sender": sender.data['id'],
        "transfer_amount": transfer_amount,
    }
    response = authorized_client.post(f"/wallets/{created_wallet.data['name']}/transactions/", post_data)
    assert response.status_code == result
