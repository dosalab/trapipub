import json
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from tracker_api.models import Carrier,Order,Customer

@pytest.mark.django_db
def test_carrier_create_with_no_merchant(client, carrier_data):
    user = User.objects.create_user("user", "useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:carrier'), carrier_data)
    assert response.status_code == 403

@pytest.mark.django_db(transaction=True)
def test_carrier_create_by_merchant(merchant_client, carrier_data,load_site):
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 201


@pytest.mark.django_db(transaction=True)
def test_carrier_creation_with_existing_username(merchant_client, carrier_data,load_site):
    response1 = merchant_client.post(reverse('tracker_api:carrier'),
                                     carrier_data)
    response2 = merchant_client.post(reverse('tracker_api:carrier'),
                                     carrier_data)
    assert response1.status_code == 201
    assert response2.status_code == 409

@pytest.mark.django_db(transaction=True)
def test_carrier_create_bad_email(merchant_client, carrier_data,load_site):
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
   
@pytest.mark.django_db(transaction=True)
def test_carrier_create_bad_name(merchant_client, carrier_data,load_site):
    # without name
    del carrier_data['name']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400
   
@pytest.mark.django_db(transaction=True)
def test_carrier_create_bad_phone(merchant_client, carrier_data,load_site):
    # without phone
    del carrier_data['phone']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400

    # Use bad phone
    # carrier_data['phone'] = "123"
    # response = merchant_client.post(reverse('tracker_api:carrier'),
    #                                 carrier_data)
    # assert response.status_code == 400

@pytest.mark.django_db(transaction=True)
def test_carrier_create_bad_location(merchant_client, carrier_data,load_site):
    # without location
    del carrier_data['location']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 201
    
@pytest.mark.django_db(transaction=True)
def test_carrier_creation_bad_username(merchant_client, carrier_data):
    #without user name
    del carrier_data['username']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400
    
@pytest.mark.django_db(transaction=True)
def test_all_carriers_of_merchant(merchant_client,load_site):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier1", phone="98766767",
                           location="india",
                           merchant=merchant, user=cu1, slug="carrier1merchant1")
    cu2 = User.objects.create_user("carrier2", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrer2", phone="99999999",
                           location="palakkad", merchant=merchant, user=cu2, slug="carrier2merchant1")
    cu3 = User.objects.create_user("carrier3", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrer3",
                           phone="99999999",
                           location="kerala", merchant=merchant, user=cu3, slug="carrier3merchant1")
    response = merchant_client.get(reverse('tracker_api:carrier'))
    actual = json.loads(response.content.decode('utf-8'))
    expected = [{"url": "http://testserver/api/v1/carriers/carrier3merchant1"},
                {"url": "http://testserver/api/v1/carriers/carrier2merchant1"},
                {"url": "http://testserver/api/v1/carriers/carrier1merchant1"}]
    assert actual == expected
   
@pytest.mark.django_db(transaction=True)
def test_details_of_carrier(merchant_client,load_site):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier", phone="9656888871",
                           location="kozikkod", merchant=merchant, user=cu1,slug="carrier1merchant1")
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=['carrier1merchant1']))
    assert response.data == {"location":"kozikkod", "name":"carrier",
                             "phone":"9656888871", "email":"user@tracker.com"}
    # Wrong args
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=[2]))
    assert response.status_code == 404

@pytest.mark.django_db(transaction=True)
def test_change_name_of_carrier (merchant_client,load_site):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier", phone="9656888871",
                           location="kozikkod", merchant=merchant, user=cu1,slug="carrier1merchant1")

    merchant_client.patch(reverse('tracker_api:carrierdetail',
                                  args=["carrier1merchant1"]), {"name":"new name"})
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=["carrier1merchant1"]))
    assert response.data == {"location":"kozikkod", "name":"new name",
                             "phone":"9656888871", "email":"user@tracker.com"}
    

@pytest.mark.django_db(transaction=True)
def test_change_phone_of_carrier(merchant_client, load_site):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier", phone="9656888871",
                           location="kozikkod", merchant=merchant, user=cu1, slug="carrier1merchant1")
    merchant_client.patch(reverse('tracker_api:carrierdetail',
                                  args=["carrier1merchant1"]), {"phone":"+9999999999"})
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=["carrier1merchant1"]))
    assert response.data == {"location":"kozikkod", "name":"carrier",
                             "phone":"+9999999999", "email":"user@tracker.com"}
     

@pytest.mark.django_db(transaction=True)
def test_change_location_of_carrier(merchant_client,load_site):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier", phone="9656888871",
                           location="kozikkod", merchant=merchant, user=cu1,slug="carrier1merchant1")

    merchant_client.patch(reverse('tracker_api:carrierdetail',
                                  args=["carrier1merchant1"]), {"location":"kerala"})
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=["carrier1merchant1"]))
    assert response.data == {"location":"kerala", "name":"carrier",
                             "phone":"9656888871", "email":"user@tracker.com"}

# /customer
@pytest.mark.django_db(transaction=True)
def test_cutomer_create_with_no_merchant(client,customer_data):
    user = User.objects.create_user("user", "useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:customer'), customer_data)
    assert response.status_code == 403


@pytest.mark.django_db(transaction=True)
def test_customer_create_by_merchant(merchant_client, customer_data,load_site):
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 201

@pytest.mark.django_db(transaction=True)
def test_customer_creation_bad_username(merchant_client, customer_data,load_site):
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

@pytest.mark.django_db(transaction=True)
def test_customer_creation_bad_name(merchant_client, customer_data):
    del customer_data['name']
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 400

@pytest.mark.django_db(transaction=True)
def test_customer_creation_bad_phone(merchant_client, customer_data):
    # customer_data['phone'] == "00000"
    # response = merchant_client.post(reverse('tracker_api:customer'),
    #                                 customer_data)
    # assert response.status_code == 400

    # without phone
    del customer_data['phone']
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 400

#/ orders /
@pytest.mark.django_db(transaction=True)
def test_order_create_with_no_merchant(load_site,client,order_data):
    user = User.objects.create_user("user", "useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:customer'), order_data)
    assert response.status_code == 403

@pytest.mark.django_db(transaction=True)
def test_order_create_by_merchant(load_site,merchant_client,order_data):
    response = merchant_client.post(reverse('tracker_api:orders'),
                                    order_data)

    assert response.status_code == 201

@pytest.mark.django_db(transaction=True)
def test_order_creat_bad_customer(load_site, merchant_client, order_data):
    #Wrong customer id
    order_data['customer'] = "2"
    response = merchant_client.post(reverse('tracker_api:orders'),
                                    order_data)
    assert response.status_code == 400

    # without customer
    del order_data["customer"]
    response = merchant_client.post(reverse('tracker_api:orders'),
                                    order_data)

    assert response.status_code == 400

@pytest.mark.django_db(transaction=True)
def test_order_creat_bad_amount(load_site, merchant_client, order_data):
    del order_data["amount"]
    response = merchant_client.post(reverse('tracker_api:orders'),
                                    order_data)
    assert response.status_code == 400

@pytest.mark.django_db(transaction=True)
def test_order_creat_bad_invoice(load_site, merchant_client, order_data):
    del order_data["invoice_number"]
    response = merchant_client.post(reverse('tracker_api:orders'),
                                    order_data)
    assert response.status_code == 400
    
@pytest.mark.django_db(transaction=True)
def test_all_orders_of_merchant(merchant_client,load_site):
    merchant = User.objects.get(username="newuser").merchant
    ur = User.objects.create(username = "customeruser",
                               password = "aaasssddd",
                               email = "customer@tracker.com")
    customer = Customer.objects.create(name="cusomer",
                                       address="customeraddress" ,
                                       phone = "+9999999999",
                                       user = ur,
                                       merchant=merchant)
    Order.objects.create(merchant=merchant, customer=customer,slug="1010",
                         notes = "items1", amount=100, invoice_number="1010")
    
    Order.objects.create(merchant=merchant, customer=customer,slug="1011",
                         notes = "items2", amount=1000, invoice_number="1011")
    
    Order.objects.create(merchant=merchant, customer=customer,
                         notes = "items4", amount=0.5, invoice_number="1012")
    response = merchant_client.get(reverse('tracker_api:orders'))
    
    expected = [{'url': 'http://testserver/api/v1/orders/slug'},
                {'url': 'http://testserver/api/v1/orders/1011'},
                {'url': 'http://testserver/api/v1/orders/1010'}]
    actual = json.loads(response.content.decode('utf-8'))
    assert expected == actual


@pytest.mark.django_db(transaction=True)
def test_details_order(merchant_client,load_site):
    merchant = User.objects.get(username="newuser").merchant
    usr = User.objects.create(username = "customeruser",
                               password = "aaasssddd",
                               email = "customer@tracker.com")
    customer = Customer.objects.create(name="cusomer",
                                       address="customeraddress" ,
                                       phone = "+9999999999",
                                       user = usr,
                                       merchant=merchant)
    Order.objects.create(merchant=merchant, customer=customer,slug="1010",
                         notes = "items1", amount=100, invoice_number="1010")
    response = merchant_client.get(reverse('tracker_api:orderdetail',
                                   args=['1010']))
    del response.data["date"]
    expected = {"invoice_number":"1010","amount":"100.00","customer":"slug","notes":"items1"}
    assert response.data == expected
#/ deliveries /
@pytest.mark.django_db(transaction=True)
def test_deliveries_create_with_no_merchant(load_site,client,delivery_data):
    user = User.objects.create_user("user", "useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:delivery'), delivery_data)
    assert response.status_code == 403


@pytest.mark.django_db(transaction=True)
def test_deliveries_create_by_merchant(load_site, merchant_client, delivery_data):
    response = merchant_client.post(reverse('tracker_api:delivery'),
                                    delivery_data)
    assert response.status_code == 201

@pytest.mark.django_db(transaction=True)
def test_deliveries_bad_order(load_site, merchant_client, delivery_data):
    # Same order
    merchant_client.post(reverse('tracker_api:delivery'),
                         delivery_data)
    response = merchant_client.post(reverse('tracker_api:delivery'),
                                    delivery_data)
    assert response.status_code == 400

    # Without Order
    del delivery_data["order"]
    response = merchant_client.post(reverse('tracker_api:delivery'),
                                    delivery_data)
    assert response.status_code == 400

@pytest.mark.django_db(transaction=True)
def test_deliveries_bad_carrier(load_site,merchant_client, delivery_data):
    # Without carrier
    del delivery_data["carrier"]
    response = merchant_client.post(reverse('tracker_api:delivery'),
                                    delivery_data)
    assert response.status_code == 400



    
