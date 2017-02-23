import json
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from tracker_api.models import Carrier, Order, Customer, DeliveryStatus

#CARRIER CREATION
@pytest.mark.django_db
def test_carrier_create_with_no_merchant(client, carrier_data):
    User.objects.create_user("user", "useraddress", "aaasssddd")
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
def test_carrier_create_bad_username(merchant_client, carrier_data):
    response1 = merchant_client.post(reverse('tracker_api:carrier'),
                                     carrier_data)
    response2 = merchant_client.post(reverse('tracker_api:carrier'),
                                     carrier_data)
    assert response1.status_code == 201
    assert response2.status_code == 409

    #without user name
    del carrier_data['username']
    response = merchant_client.post(reverse('tracker_api:carrier'),
                                    carrier_data)
    assert response.status_code == 400

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

# GET ALL CARRIERS
@pytest.mark.django_db
def test_all_carriers_of_merchant(merchant_client, client):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier1", phone="98766767",
                           merchant=merchant,
                           user=cu1,
                           slug="carrier1merchant1")
    cu2 = User.objects.create_user("carrier2", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrer2",
                           phone="99999999",
                           merchant=merchant,
                           user=cu2, slug="carrier2merchant1")
    cu3 = User.objects.create_user("carrier3", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrer3",
                           phone="99999999",
                           merchant=merchant,
                           user=cu3, slug="carrier3merchant1")
    response = merchant_client.get(reverse('tracker_api:carrier'))
    actual = json.loads(response.content.decode('utf-8'))
    expected = [{"url": "http://testserver/api/v1/carriers/carrier3merchant1"},
                {"url": "http://testserver/api/v1/carriers/carrier2merchant1"},
                {"url": "http://testserver/api/v1/carriers/carrier1merchant1"}]
    assert actual == expected

    # non user try to get carriers
    response = client.post(reverse('tracker_api:carrier'))
    assert response.status_code == 401

# GET DETAILS OF A CARRIER
@pytest.mark.django_db
def test_details_of_new_carrier(merchant_client):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier", phone="9656888871",
                           merchant=merchant,
                           user=cu1, slug="carrier1merchant1")
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=['carrier1merchant1']))
    assert response.data == {"name":"carrier",
                             "phone":"9656888871",
                             "email":"user@tracker.com",
                             "delivery":"", "point":None}
    # Wrong args
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=[2]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_carrier_ongoing_deliveries(merchant_client, delivery_data):
    merchant_client.post(reverse('tracker_api:delivery'),
                         delivery_data)
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=["carrierusermerchant1"]))
    assert response.data == {"point": {'type': 'Point',
                                       'coordinates': (75.955277777778, 11.136944444444)},
                             "name":"carrier",
                             "phone":"99798798", "email":"test@example.com",
                             "delivery":['/deliveries/1010carrier']}


@pytest.mark.django_db
def test_carrier_free(merchant_client,carrier_data):
    merchant_client.post(reverse('tracker_api:carrier'),
                         carrier_data)
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=["carrierusermerchant1"]))
    assert response.data == {"point":{'type': 'Point',
                                      'coordinates': (75.955277777778, 11.136944444444)},
                             "name":"carrier",
                             "phone":"99798798",
                             "email":"test@example.com",
                             "delivery":""}

# CHANGE CARRIER DETAILS
@pytest.mark.django_db
def test_change_name_of_carrier_by_carrier (carrier_client, merchant_client):
    carrier_client.patch(reverse('tracker_api:carrierdetail',
                                 args=["carrierusermerchant1"]),
                         {"name":"new name"})
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=["carrierusermerchant1"]))
    assert response.data == {'point': {'type': 'Point',
                                       'coordinates': (75.955277777778, 11.136944444444)},
                             "name":"new name",
                             "phone":"99798798",
                             "email":"test@example.com",
                             "delivery":""}
@pytest.mark.django_db
def test_try_to_change_detalis_without_data (carrier_client, merchant_client):
    response = carrier_client.patch(reverse('tracker_api:carrierdetail',
                                            args=["carrierusermerchant1"]),
                                    {})
    assert response.status_code == 400
@pytest.mark.django_db
def test_change_name_of_carrier_by_other_carrier (carrier_client, merchant_client):
    merchant = User.objects.get(username="newuser").merchant
    cu1 = User.objects.create_user("carrier1", "user@tracker.com", "aaasssddd")
    Carrier.objects.create(name="carrier1", phone="98766767",
                           merchant=merchant,
                           user=cu1,
                           slug="carrier1merchant1")
    
    response = carrier_client.patch(reverse('tracker_api:carrierdetail',
                                            args=["carrier1merchant1"]),
                                    {"name":"new name"})
    assert response.status_code == 400
    
@pytest.mark.django_db    
def test_change_name_of_carrier_by_merchant (carrier_client, merchant_client):
    merchant_client.patch(reverse('tracker_api:carrierdetail',
                                  args=["carrierusermerchant1"]),
                          {"name":"new name"})
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=["carrierusermerchant1"]))
    assert response.data == {'point': {'type': 'Point',
                                       'coordinates': (75.955277777778, 11.136944444444)},
                             "name":"new name",
                             "phone":"99798798",
                             "email":"test@example.com",
                             "delivery":""}

   
@pytest.mark.django_db    
def create_delivery_from_carrier_id (order_data,carrier_data, merchant_client):
    merchant_client.post(reverse('tracker_api:orders'),
                         order_data)

    response = merchant_client.post(reverse('tracker_api:carrierdeliveries',
                                            args=["carrierusermerchant1"]),
                                    {"order":""})
    import pdb;pdb.set_trace()
    assert response.data == {'point': {'type': 'Point',
                                       'coordinates': (75.955277777778, 11.136944444444)},
                             "name":"new name",
                             "phone":"99798798",
                             "email":"test@example.com",
                             "delivery":""}

@pytest.mark.django_db
def test_change_phone_of_carrier(merchant_client, carrier_client):
    carrier_client.patch(reverse('tracker_api:carrierdetail',
                                 args=["carrierusermerchant1"]),
                         {"phone":"+9999999999"})
    response = merchant_client.get(reverse('tracker_api:carrierdetail',
                                           args=["carrierusermerchant1"]))
    assert response.data == {'point': {'type': 'Point',
                                       'coordinates': (75.955277777778, 11.136944444444)},
                             "name":"carrier",
                             "phone":"+9999999999",
                             "email":"test@example.com",
                             "delivery":""}

# /customer
@pytest.mark.django_db
def test_cutomer_create_with_no_merchant(client, customer_data):
    User.objects.create_user("user", "useraddress", "aaasssddd")
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
#customer register
@pytest.mark.django_db
def test_customer_registration_by_merchant(merchant_client, customer_data):
    merchant_client.post(reverse('tracker_api:customer'),
                         customer_data)
    response = merchant_client.post(reverse('tracker_api:customerregister',
                                            args=["91239798798"]),
                                    {"email":"customer@tracker.com"})
    assert response.status_code == 200

@pytest.mark.django_db
def test_customer_registration_without_email(merchant_client, customer_data):
    merchant_client.post(reverse('tracker_api:customer'),
                         customer_data)
    response = merchant_client.post(reverse('tracker_api:customerregister',
                                            args=["91239798798"]), {})
    assert response.status_code == 200

@pytest.mark.django_db
def test_details_of_customer(merchant_client, customer_data):
    merchant_client.post(reverse('tracker_api:customer'),
                         customer_data)
    response = merchant_client.get(reverse('tracker_api:customerdetails',
                                           args=["91239798798"]))
    assert response.data == {'address': 'Calicut',
                             'phone': '91239798798',
                             'name': 'customer1',
                             'point': {'type': 'Point',
                                       'coordinates': (75.955277777778,
                                                       11.136944444444)}}


@pytest.mark.django_db
def test_customer_creation_bad_name(merchant_client, customer_data):
    del customer_data['name']
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_customer_creation_bad_address(merchant_client, customer_data):
    del customer_data['address']
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_customer_creation_bad_phone(merchant_client, customer_data):

    # without phone
    del customer_data['phone']
    response = merchant_client.post(reverse('tracker_api:customer'),
                                    customer_data)
    assert response.status_code == 400

#Change customer detailss
@pytest.mark.django_db
def test_change_customer_name(merchant_client, customer_data):
    merchant_client.post(reverse('tracker_api:customer'),
                         customer_data)
    response = merchant_client.patch(reverse('tracker_api:customerdetails',
                                             args=["91239798798"]),
                                     {"name":"new name"})
    assert response.json() == {'phone': '91239798798',
                              'name': 'new name', 'address': 'Calicut',
                              'point': {'coordinates': [75.955277777778, 11.136944444444],
                                        'type': 'Point'}}

@pytest.mark.django_db
def test_change_customer_address(merchant_client, customer_data):
    merchant_client.post(reverse('tracker_api:customer'),
                         customer_data)
    response = merchant_client.patch(reverse('tracker_api:customerdetails',
                                             args=["91239798798"]),
                                     {"address":"palakkad"})
    assert response.json() == {'name': 'customer1',
                              'address': 'palakkad', 'phone': '91239798798',
                              'point': {'coordinates': [76.6614, 10.7676],
                                        'type': 'Point'}}


    
#/ orders /
@pytest.mark.django_db
def test_order_create_with_no_merchant(client,order_data):
    User.objects.create_user("user", "useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:customer'), order_data)
    assert response.status_code == 403

@pytest.mark.django_db
def test_order_creat_by_merchant(merchant_client,order_data):
    response = merchant_client.post(reverse('tracker_api:orders'),
                                    order_data)

    assert response.status_code == 201

@pytest.mark.django_db
def test_order_creat_bad_customer(merchant_client, order_data):
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


@pytest.mark.django_db
def test_order_creat_bad_amount(merchant_client, order_data):
    del order_data["amount"]
    response = merchant_client.post(reverse('tracker_api:orders'),
                                    order_data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_order_creat_bad_invoice(merchant_client, order_data):
    del order_data["invoice_number"]
    response = merchant_client.post(reverse('tracker_api:orders'),
                                    order_data)
    assert response.status_code == 400
    
@pytest.mark.django_db
def test_all_orders_of_merchant(merchant_client):
    merchant = User.objects.get(username="newuser").merchant
    usr = User.objects.create(username="customeruser",
                              password="aaasssddd",
                              email="customer@tracker.com")
    customer = Customer.objects.create(name="cusomer",
                                       phone="+9999999999",
                                       user=usr)
    Order.objects.create(merchant=merchant, customer=customer, slug="1010",
                         notes="items1", amount=100, invoice_number="1010")
    
    Order.objects.create(merchant=merchant, customer=customer, slug="1011",
                         notes="items2", amount=1000, invoice_number="1011")
    
    Order.objects.create(merchant=merchant, customer=customer,
                         notes="items4", amount=0.5, invoice_number="1012")
    response = merchant_client.get(reverse('tracker_api:orders'))

    expected = [{'url': 'http://testserver/api/v1/orders/slug'},
                {'url': 'http://testserver/api/v1/orders/1011'},
                {'url': 'http://testserver/api/v1/orders/1010'}]
    actual = json.loads(response.content.decode('utf-8'))
    assert expected == actual


@pytest.mark.django_db
def test_details_order(merchant_client):
    merchant = User.objects.get(username="newuser").merchant
    usr = User.objects.create(username="customeruser",
                              password="aaasssddd",
                              email="customer@tracker.com")
    customer = Customer.objects.create(name="cusomer",
                                       phone="+9999999999",
                                       user=usr)
    Order.objects.create(merchant=merchant, customer=customer, slug="1010",
                         notes="items1", amount=100, invoice_number="1010")
    response = merchant_client.get(reverse('tracker_api:orderdetail',
                                           args=['1010']))
    del response.data["date"]
    expected = {"invoice_number":"1010",
                "amount":"100.00",
                "customer":"slug",
                "notes":"items1",
                "from_address":"",
                "to_address":"",
                "from_point":None,
                "to_point":None}

    assert response.data == expected


@pytest.mark.django_db
def test_details_customer_order(merchant_client,order_data):
    merchant_client.post(reverse('tracker_api:orders'),
                         order_data)

    response = merchant_client.get(reverse('tracker_api:customeroderdetails',
                                           args=["91239798798"]))
   
    assert response.json() == {'address': 'Calicut',
                               'name': 'customer1', 'phone': '91239798798',
                               'order_set': ['1010'],
                               'point': {'coordinates': [75.955277777778, 11.136944444444],
                                         'type': 'Point'}}
# DELIVERIES
@pytest.mark.django_db
def test_create_deliveries_from_carrier(carrier_data,merchant_client,order_data):
    merchant_client.post(reverse('tracker_api:orders'),
                         order_data)
    merchant_client.post(reverse('tracker_api:carrier'),
                         carrier_data)
    DeliveryStatus.objects.create(name="Assigned")
    response = merchant_client.post(reverse('tracker_api:carrierdeliveries',
                                            args=["carrierusermerchant1"]),
                                    {"order":"1010"})
   
    assert response.json() == {'url': 'http://testserver/api/v1/deliveries/1010carrier'}


@pytest.mark.django_db
def test_list_deliveries_of_a_carrier(carrier_data,merchant_client,order_data):
    merchant_client.post(reverse('tracker_api:orders'),
                         order_data)
    merchant_client.post(reverse('tracker_api:carrier'),
                         carrier_data)
    DeliveryStatus.objects.create(name="Assigned")
    merchant_client.post(reverse('tracker_api:carrierdeliveries',
                                 args=["carrierusermerchant1"]),
                         {"order":"1010"})
    response = merchant_client.get(reverse('tracker_api:carrierdeliveries',
                                           args=["carrierusermerchant1"]))
    assert response.json() == {'deliveries': ['/deliveries/1010carrier']}


@pytest.mark.django_db
def test_list_deliveries_by_status_of_carrier(carrier_data,merchant_client,order_data):
    merchant_client.post(reverse('tracker_api:orders'),
                         order_data)
    merchant_client.post(reverse('tracker_api:carrier'),
                         carrier_data)
    DeliveryStatus.objects.create(name="Assigned")
    merchant_client.post(reverse('tracker_api:carrierdeliveries',
                                 args=["carrierusermerchant1"]),
                         {"order":"1010"})
    response = merchant_client.get(reverse('tracker_api:carrierdeliverystatus',
                                           args=["carrierusermerchant1","Assigned"]))
    assert response.json() == [{'delivery': 'http://testserver/api/v1/deliveries/1010carrier',
                                'order': 'http://testserver/api/v1/orders/1010carrier',
                                'status': 'Assigned', 'location': 'SRID=4326;POINT (75.95527777777799 11.136944444444)'}]


@pytest.mark.django_db
def test_deliveries_create_with_no_merchant(client, delivery_data):
    User.objects.create_user("user", "useraddress", "aaasssddd")
    token = Token.objects.get(user__username='user')
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.post(reverse('tracker_api:delivery'), delivery_data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_deliveries_create_by_merchant(merchant_client, delivery_data):
    response = merchant_client.post(reverse('tracker_api:delivery'),
                                    delivery_data)
    assert response.status_code == 201


    
@pytest.mark.django_db
def test_deliveries_bad_order(merchant_client, delivery_data):
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


@pytest.mark.django_db
def test_deliveries_bad_carrier(merchant_client, delivery_data):
    # Without carrier
    del delivery_data["carrier"]
    response = merchant_client.post(reverse('tracker_api:delivery'),
                                    delivery_data)
    assert response.status_code == 400



@pytest.mark.django_db
def test_deliveries_details(merchant_client, delivery_data):
    merchant_client.post(reverse('tracker_api:delivery'),
                         delivery_data)

    response = merchant_client.get(reverse('tracker_api:deliverydetails',
                                           args=['1010carrier']))

    assert response.json() == {'to_address': {'coordinates': [75.955277777778, 11.136944444444], 'type': 'Point'},
                               'progress': {'features': [{'properties': {}, 'geometry': {'coordinates': [75.955277777778, 11.136944444444],
                                                                                         'type': 'Point'},
                                                          'type': 'Feature'},
                                                         {'properties': {}, 'geometry': {'coordinates': [75.955277777778, 11.136944444444],
                                                                                         'type': 'Point'}, 'type': 'Feature'},
                                                         {'properties': {}, 'geometry': {'coordinates': [75.955277777778, 11.136944444444],
                                                                                         'type': 'Point'}, 'type': 'Feature'}],
                                            'type': 'FeatureCollection'},
                               'current_location': {'coordinates': [75.955277777778, 11.136944444444], 'type': 'Point'},
                               'status': 'Assigned', 'customer': '91239798798',
                               'from_address': {'coordinates': [75.955277777778, 11.136944444444], 'type': 'Point'},
                               'carrier': {'url': 'http://testserver/api/v1/carriers/carrierusermerchant1'},
                               'last_updated': '2017-02-23T00:00:00Z',
                               'order': {'url': 'http://testserver/api/v1/orders/1010'}}


@pytest.mark.django_db
def test_deliveries_status_details(merchant_client, delivery_data):
    merchant_client.post(reverse('tracker_api:delivery'),
                         delivery_data)
    
    response = merchant_client.get(reverse('tracker_api:deliverystatus',
                                   args=["Assigned"]))
    assert response.json() == [{'status': 'Assigned',
                                'url': 'http://testserver/api/v1/deliveries/1010carrier'}]


#Change password

@pytest.mark.django_db
def test_change_password(merchant_client):
    response = merchant_client.post(reverse('tracker_api:change_password'),
                                    {"old_password" :"test_password",
                                     "new_password" :'password123'})
    assert response.status_code == 200

@pytest.mark.django_db
def wrong_data_password_change(merchant_client):
    response = merchant_client.post(reverse('tracker_api:change_password'),
                                    {"old_password" :"test_password"})
    assert response.status_code == 200
