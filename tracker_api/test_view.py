import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .views import carrierView
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import json
from .models import Merchant,Carrier
@pytest.mark.django_db
def test_carrier_create_with_no_merchant(client):
    user=User.objects.create_user("user","useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'phone':"99798798",'location':"here",'user':user,'merchant':"null"})
    assert response.status_code == 403

@pytest.mark.django_db
def test_carrier_create_by_merchant(client):
    merchant=client.post(reverse('registration_register'),{"username":"newuser","email":"user@gmail.com","password1":"aaasssddd","password2":'aaasssddd',"name":"merchant1",'address':"merchantaddress"})
    merchant=User.objects.get(username="newuser").merchant
    token = Token.objects.get(user__username='newuser')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'phone':"99798798",'location':"here","username":"carrieruser","password":"aaasssddd","email":"carrier@gmail.com"})
    assert response.status_code == 201


@pytest.mark.django_db
def test_carrier_creation_with_existing_username(client):
    merchant=client.post(reverse('registration_register'),{"username":"newuser","email":"user@gmail.com","password1":"aaasssddd","password2":'aaasssddd',"name":"merchant1",'address':"merchantaddress"})
    merchant=User.objects.get(username="newuser").merchant
    token = Token.objects.get(user__username='newuser')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response1 = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'phone':"99798798",'location':"here","username":"carrieruser","password":"aaasssddd","email":"carrier@gmail.com"})
    response2 = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'phone':"99798798",'location':"here","username":"carrieruser","password":"aaasssddd","email":"carrier@gmail.com"})
    assert response1.status_code == 201
    assert response2.status_code == 409



@pytest.mark.django_db
def test_carrier_creation_without_proper_data(client):
    merchant=client.post(reverse('registration_register'),{"username":"newuser","email":"user@gmail.com","password1":"aaasssddd","password2":'aaasssddd',"name":"merchant1",'address':"merchantaddress"})
    merchant=User.objects.get(username="newuser").merchant
    token = Token.objects.get(user__username='newuser')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    # email
    email = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'phone':"99798798",'location':"here","username":"carrieruser","password":"aaasssddd"})
    # name
    name = client.post(reverse('tracker_api:carrier'),{'phone':"99798798",'location':"here","username":"carrieruser","password":"aaasssddd","email":"carrier@gmail.com"})
    # phone
    phone = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'location':"here","username":"carrieruser","password":"aaasssddd","email":"carrier@gmail.com"})
    # location
    location = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'phone':"99798798","username":"carrieruser","password":"aaasssddd","email":"carrier@gmail.com"})
    username = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'phone':"99798798",'location':"here","password":"aaasssddd","email":"carrier@gmail.com"})
    password = client.post(reverse('tracker_api:carrier'),{'name':"carrer",'phone':"99798798",'location':"here","username":"carrieruser","email":"carrier@gmail.com"})
    assert email.status_code == 400
    assert name.status_code == 400
    assert phone.status_code == 400
    assert username.status_code == 400
    assert password.status_code == 400
    assert location.status_code == 201
    

    
@pytest.mark.django_db
def test_all_carriers_of_merchant(client):
    user=User.objects.create_user("user","user@tracker.com", "aaasssddd")
    Merchant.objects.create(name="merchant1",address="merchantaddress",user=user)
    merchant=User.objects.get(username="user").merchant
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    cu1=User.objects.create_user("carrier1","user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrer1",phone="9656888871",location="kozikkod",merchant=merchant,user=cu1)
    
    cu2=User.objects.create_user("carrier2","user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrer2",phone="99999999",location="palakkad",merchant=merchant,user=cu2)

    cu3=User.objects.create_user("carrier3","user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrer3",phone="99999999",location="kerala",merchant=merchant,user=cu3)

    response = client.get(reverse('tracker_api:get_carriers'))
    op= [{"url": "http://testserver/api/v1/carrier/1"},{ "url": "http://testserver/api/v1/carrier/2"},{ "url": "http://testserver/api/v1/carrier/3"}]
    assert response.data == op
    



@pytest.mark.django_db
def test_details_of_carrier(client):
    user=User.objects.create_user("user","user@tracker.com", "aaasssddd")
    Merchant.objects.create(name="merchant1",address="merchantaddress",user=user)
    merchant=User.objects.get(username="user").merchant
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    cu1=User.objects.create_user("carrier1","user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier",phone="9656888871",location="kozikkod",merchant=merchant,user=cu1)
   
    response = client.get(reverse('tracker_api:carrierdetail',args=[1]))
    op = {"id":1,"location":"kozikkod","name":"carrier","phone":"9656888871"}
    assert response.data == op


@pytest.mark.django_db
def test_change_details_of_carrier(client):
    user=User.objects.create_user("user","user@tracker.com", "aaasssddd")
    Merchant.objects.create(name="merchant1",address="merchantaddress",user=user)
    merchant=User.objects.get(username="user").merchant
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    cu1=User.objects.create_user("carrier1","user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier",phone="9656888871",location="kozikkod",merchant=merchant,user=cu1)

    response = client.get(reverse('tracker_api:carrierdetail',args=[1]))
    assert response.data ==  {"id":1,"location":"kozikkod","name":"carrier","phone":"9656888871"}

    client.patch(reverse('tracker_api:carrierdetail',args=[1]),{"name":"new name"})
    response = client.get(reverse('tracker_api:carrierdetail',args=[1]))
    assert response.data ==  {"id":1,"location":"kozikkod","name":"new name","phone":"9656888871"}

   
