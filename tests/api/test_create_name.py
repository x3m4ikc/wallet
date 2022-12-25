import pytest
from rest_framework.test import APIClient
from pytest_mock import mocker
from wallets.models import User
from wallets.views import name


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
def test_name(authorized_client):
    print(mocker.__dict__)
    name = mocker.Mock(return_value="AAAAAAAA")
    payload = {
        "type": "VISA",
        "currency": "USD"
    }
    response = authorized_client.post("/wallets/", payload)
    return response


# norm generate
# exceptation wrong with mock
# mock this ''.join(random.choice(letters) for _ in range(8)) (without digits)
