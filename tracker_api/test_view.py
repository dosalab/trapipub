import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .views import carrierView
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_carrier_view_with_no_merchant(client):
    user=User.objects.create_user("user","useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'phone':"99798798",'location':"here",'user':user,'merchant':"null"})
    assert response.status_code == 403
    
