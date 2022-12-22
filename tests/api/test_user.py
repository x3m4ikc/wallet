import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    """Register test"""
    payload = {
        "email": "admin1@admin.com",
        "password": "ad109299ad",
        "username": "admin1"
    }

    response = client.post("/auth/users/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_login_user_fail():
    """Wrong login test"""
    payload = {
        "name": "admin",
        "password": "admin12",
    }
    response = client.post("drf-auth/login/", payload)
    assert response.status_code == 404


@pytest.mark.django_db
def test_login_user():
    """Login test"""
    payload = {
        "name": "admin",
        "password": "admin"
    }
    response = client.post("/drf-auth/login/", payload)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_logout():
#     """Logout test"""
#     response = client.post()
#     assert response.status_code == 200
