import json
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Carrier

@pytest.mark.django_db
def test_carrier_create_with_no_merchant(client, carrier_data):
    user = User.objects.create_user("user", "useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:carrier'), carrier_data)
    assert response.status_code == 403

@pytest.mark.django_db
def test_carrier_create_by_merchant(merchant_client, carrier_data):
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_carrier_creation_with_existing_username(merchant_client, carrier_data):
    response1 = merchant_client.post(reverse('tracker_api:carrier'),
                                     carrier_data)
    response2 = merchant_client.post(reverse('tracker_api:carrier'),
                                     carrier_data)
    assert response1.status_code == 201
    assert response2.status_code == 409

@pytest.mark.django_db
def test_carrier_create_bad_email(merchant_client, carrier_data):
    # Use bad email
    carrier_data['email'] = "bad_email_address"
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400, "Didn't fail when email was invalid"

    # Without email
    del carrier_data['email']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400, "Didn't fail when email was not present"
   
@pytest.mark.django_db
def test_carrier_create_bad_name(merchant_client, carrier_data):
    # without name
    del carrier_data['name']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400
   
@pytest.mark.django_db
def test_carrier_create_bad_phone(merchant_client, carrier_data):
    # without phone
    del carrier_data['phone']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400

    # Use bad phone
    carrier_data['phone'] = "123"
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_carrier_create_bad_location(merchant_client, carrier_data):
    # without location
    del carrier_data['location']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 201
    
@pytest.mark.django_db
def test_carrier_creation_bad_username(merchant_client, carrier_data):
    #without user name
    del carrier_data['username']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400
    
@pytest.mark.django_db
def test_all_carriers_of_merchant(merchant_client):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier1", phone="98766767",
                           location="india",
                           merchant=merchant, user=cu1)
    cu2 = User.objects.create_user("carrier2", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrer2", phone="99999999",
                           location="palakkad", merchant=merchant, user=cu2)
    cu3 = User.objects.create_user("carrier3", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrer3",
                           phone="99999999",
                           location="kerala", merchant=merchant, user=cu3)
    response = merchant_client.get(reverse('tracker_api:carrier'))
    assert  json.loads(response.content.decode('utf-8')) == [
        {"url": "http://testserver/api/v1/carriers/1"},
        {"url": "http://testserver/api/v1/carriers/2"},
        {"url": "http://testserver/api/v1/carriers/3"}]
   
@pytest.mark.django_db
def test_details_of_carrier(merchant_client):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier", phone="9656888871",
                           location="kozikkod", merchant=merchant, user=cu1)
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=[1]))
    assert response.data == {"id":1, "location":"kozikkod", "name":"carrier",
                             "phone":"9656888871", "email":"user@tracker.com"}
    # Wrong args
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=[2]))
    assert response.status_code == 404

@pytest.mark.django_db
def test_change_name_of_carrier (merchant_client):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier", phone="9656888871",
                           location="kozikkod", merchant=merchant, user=cu1)

    merchant_client.patch(reverse('tracker_api:carrierdetail',
                                  args=[1]), {"name":"new name"})
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=[1]))
    assert response.data == {"id":1, "location":"kozikkod", "name":"new name",
                             "phone":"9656888871", "email":"user@tracker.com"}
    

@pytest.mark.django_db
def test_change_phone_of_carrier(merchant_client):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier", phone="9656888871",
                           location="kozikkod", merchant=merchant, user=cu1)
    merchant_client.patch(reverse('tracker_api:carrierdetail',
                                  args=[1]), {"phone":"+9999999999"})
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=[1]))
    assert response.data == {"id":1, "location":"kozikkod", "name":"carrier",
                             "phone":"+9999999999", "email":"user@tracker.com"}
     

@pytest.mark.django_db
def test_change_location_of_carrier(merchant_client):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier", phone="9656888871",
                           location="kozikkod", merchant=merchant, user=cu1)

    merchant_client.patch(reverse('tracker_api:carrierdetail',
                                  args=[1]), {"location":"kerala"})
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=[1]))
    assert response.data == {"id":1, "location":"kerala", "name":"carrier",
                             "phone":"9656888871", "email":"user@tracker.com"}

# /customer
@pytest.mark.django_db
def test_cutomer_create_with_no_merchant(client,customer_data):
    user = User.objects.create_user("user", "useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:customer'), customer_data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_customer_create_by_merchant(merchant_client, customer_data):
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_customer_creation_bad_username(merchant_client, customer_data):
    #already used username
    response1 = merchant_client.post(reverse('tracker_api:customer'),
                                     customer_data)
    response2 = merchant_client.post(reverse('tracker_api:customer'),
                                     customer_data)
    assert response1.status_code == 201
    assert response2.status_code == 409

   #without user name
    del customer_data['username']
    response1 = merchant_client.post(reverse('tracker_api:customer'),
                                     customer_data)
    assert response1.status_code == 400

@pytest.mark.django_db
def test_customer_creation_bad_name(merchant_client, customer_data):
    del customer_data['name']
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_customer_creation_bad_phone(merchant_client, customer_data):
    customer_data['phone'] == "00000"
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 400

    # without phone
    del customer_data['phone']
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 400

#/ orders /
@pytest.mark.django_db
def test_order_create_with_no_merchant(client,order_data):
    user = User.objects.create_user("user", "useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:customer'), order_data)
    assert response.status_code == 403

@pytest.mark.django_db
def test_order_create_by_merchant(merchant_client,order_data):
    response = merchant_client.post(reverse('tracker_api:orders'),
                                    order_data)
    assert response.status_code == 201
