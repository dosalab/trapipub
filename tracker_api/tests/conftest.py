import time
from django.core.management import call_command
from django.urls import reverse
import requests
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import pytest
from tracker_api.models import DeliveryStatus

@pytest.fixture
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("migrate")
        call_command('loaddata', 'tracker_api/tests/fixture.json')
    


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
    return {'name':"carrier",
            'phone':"99798798",
            "email" : "test@example.com",
            "username":"carrieruser",
            "password":"aaasssddd"}

@pytest.fixture
def customer_data(request):
    return{'name':"customer1",
           'phone':"+91239798798",
           'address':"india"}

@pytest.fixture
def order_data(request,merchant_client,customer_data):
    merchant_client.post(reverse('tracker_api:customer'),
                         customer_data)
    return{'customer':"91239798798",
           'notes':"include item1,2",
           'amount':"100",
           "invoice_number":"1010"}


@pytest.fixture
def delivery_data(request,merchant_client,carrier_data,order_data):
    merchant_client.post(reverse('tracker_api:carrier'),
                         carrier_data)
    merchant_client.post(reverse('tracker_api:orders'),
                         order_data)
    DeliveryStatus.objects.create(name="Assigned")
    deliv = DeliveryStatus.objects.get(name="Assigned")
    return {'order':"1010",
            'carrier':"carrierusermerchant1",
            'status':deliv}
