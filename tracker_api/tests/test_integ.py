import json
import datetime
import pytest
import requests
import sys

#host = "http://127.0.0.1:8000"
#host = "http://ec2-54-64-56-135.ap-northeast-1.compute.amazonaws.com"

@pytest.mark.django_db
def test_merchant(live_server):
    host = live_server.url
    URL = "{}/accounts/register/".format(host)
    client = requests.session()
    client.get(URL)
    csrftoken = client.cookies['csrftoken']
    
    # merchant creation 
    login_data = dict(username="newuser1234",
                      email="newuser@tracker.com",
                      password1="aaasssddd", password2="aaasssddd",
                      name="newmerchant", address="Calicut",
                      csrfmiddlewaretoken=csrftoken)
    client.post(URL, data=login_data, headers=dict(Referer=URL))

    # token
    token1 = client.post("{}/token/".format(host),
                         {'username':"newuser1234", 'password':"aaasssddd"})
    token1 = token1.json()['token']

    # carrier creation
    data =  {'name':"carrier",
             'phone':"99798798",
             "email" : "test@example.com",
             "username":"carrieruser",
             "password":"aaasssddd",
             "location":"calicut"}

    headers = {'Authorization': 'Token '+token1}
    client.post("{}/api/v1/carriers".format(host),
                data=data,
                headers=headers)
    #get a particular carrier details
    carriers = client.get('{}/api/v1/carriers/carrierusernewmerchant'.format(host),
                          headers={'Authorization':'Token '+token1})
    assert json.loads(carriers.text) == {"name":"carrier",
                                         "phone":"99798798",
                                         'point': {'coordinates': [75.955277777778, 11.136944444444], 'type': 'Point'},
                                         "email":"test@example.com",
                                         "delivery":""}

    #get all carriers
    # allcarriers= client.get('{}/api/v1/carriers'.format(host),headers = {'Authorization':'Token '+token1})
    # import pdb;pdb.set_trace()
    # assert json.loads(allcarriers.text) == [{"url":"{}/api/v1/carriers/carriernewusernewmerchant".format(host)}]
   
    # customer creation
    client.post('{}/api/v1/customers/'.format(host),
                {'name':"newcustomer",
                 'phone':"99999",
                 "address":"Calicut"},
                headers={'Authorization':'Token '+token1})

    #get all customers of a merchant
    customer = client.get('{}/api/v1/customers'.format(host),
                          headers={'Authorization':'Token '+token1})
    assert json.loads(customer.text) == []

    #get a particular customer details
    customer=client.get('{}/api/v1/customers/99999'.format(host),
                        headers={'Authorization':'Token '+token1})
    assert json.loads(customer.text) == {"name":"newcustomer",
                                         "phone":"99999",
                                         "address":'Calicut',
                                         'point': {'coordinates': [75.955277777778, 11.136944444444], 'type': 'Point'}}

    # creat an order
    order=client.post('{}/api/v1/orders'.format(host),
                      {'customer':"99999",
                       'notes':"include item1,2",
                       'amount':"100",
                       "invoice_number":"1010",
                       "from_address":"calicut",
                       "to_address":"calicut"},
                      headers={'Authorization':'Token '+token1})
    #get all orders of a merchant
    order = client.get('{}/api/v1/orders'.format(host),
                       headers={'Authorization':'Token '+token1})
    assert json.loads(order.text) == [{"url":"{}/api/v1/orders/1010".format(host)}]

    #get a particular order details
    order=client.get('{}/api/v1/orders/1010'.format(host),headers={'Authorization':'Token '+token1})
    op = json.loads(order.text)
    del op["date"]
    assert op == {"invoice_number":"1010",
                  "amount":"100.00",
                  "customer":"99999",
                  "notes":"include item1,2",
                  "from_address": "calicut",
                  "from_point": {'coordinates': [75.955277777778, 11.136944444444],'type': 'Point'},
                  "to_address": "calicut",
                  "to_point": {'coordinates': [75.955277777778, 11.136944444444],'type': 'Point'}}

    
    # creat a delivery
    client.post('{}/api/v1/deliveries'.format(host),
                {"order":"1010",
                 "carrier":"carrierusernewmerchant"},
                headers={'Authorization':'Token '+token1})
    # Get customers who orderd from a merchant
    customers = client.get('{}/api/v1/customers'.format(host),
                       headers={'Authorization':'Token '+token1})
    assert json.loads(customers.text) == [{"url":"{}/api/v1/customers/99999".format(host)}]
    # Get deliveries of a merchant
    deliveries = client.get('{}/api/v1/deliveries'.format(host),
                            headers={'Authorization':'Token '+token1})
    carriersdelivery = client.post('{}/api/v1/carriers/carrierusernewmerchant/deliveries'.format(host),
                                   {"order":"1010"},
                                   headers={'Authorization':'Token '+token1})
    deliveries = client.get('{}/api/v1/deliveries'.format(host),
                            headers={'Authorization':'Token '+token1})

