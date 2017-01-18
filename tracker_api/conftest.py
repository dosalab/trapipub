from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

import pytest


@pytest.fixture
def merchant_client(request, client):
    client.post(reverse('registration_register'),
                {"username"  :"newuser",
                 "email"     :"user@gmail.com",
                 "password1" :"test_password",
                 "password2" :'test_password',
                 "name"      :"merchant1",
                 'address'   :"merchantaddress"})
    token = Token.objects.get(user__username='newuser')
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return api_client

@pytest.fixture
def carrier_data(request):
    "Creates a valid dict of carrier data"
    return {'name':"carrer",
            'phone':"99798798",
            'location':"here",
            "email" : "test@example.com",
            "username":"carrieruser",
            "password":"aaasssddd"}

@pytest.fixture
def customer_data(request):
    return{'name':"customer1",
           'phone':"+91239798798",
           'address':"india",
           "username":"customeruser",
           "password":"aaasssddd",
           "email":"customer1@gmail.com"}

@pytest.fixture
def order_data(request,merchant_client,customer_data):
    merchant_client.post(reverse('tracker_api:customer'),
                         customer_data)
    return{'customer':"1",
           'notes':"include item1,2",
           'amount':"100",
           "invoice_number":"123"}
