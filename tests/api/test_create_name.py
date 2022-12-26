import pytest
from rest_framework.test import APIClient
# from pytest_mock import mocker
from unittest.mock import patch
from wallets.models import User
import wallets


@pytest.fixture()
def authorized_client():
    client = APIClient()
    obj = User.objects.create(username="test2",
                              password="test2",
                              email="test2@test2.com")
    obj.save()
    client.force_authenticate(user=obj)
    return client


@pytest.mark.django_db
def test_mocking_name(authorized_client):
    with patch("wallets.views.random_letters") as mocked_name:
        mocked_name.return_value = "AAAAAAAA"
        payload = {
            "type": "VISA",
            "currency": "USD",
        }
        with pytest.raises(ValueError):
            response = authorized_client.post("/wallets/", payload)
