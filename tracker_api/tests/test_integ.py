import pytest
import requests
import sys
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from tracker_api.models import Carrier,Customer,Order,Delivery
@pytest.mark.django_db
def test_merchant(server):
    URL = "http://127.0.0.1:8000/accounts/register/"
    client = requests.session()
    client.get(URL)
    csrftoken = client.cookies['csrftoken']

    # merchant creation 
    login_data = dict(username="newuser1234",email="newuser@tracker.com",password1="aaasssddd",password2="aaasssddd",name="newmerchant",address="merchantaddress", csrfmiddlewaretoken=csrftoken)
    client.post(URL, data=login_data, headers=dict(Referer=URL))
    assert  User.objects.get(username="newuser1234").merchant.name == "newmerchant"
    
    token1 = client.post('http://127.0.0.1:8000/token/',{'username':"newuser1234",'password':"aaasssddd"})
    token2 = Token.objects.get(user__username='newuser1234').key
    token1=token1.json()['token']

    assert token1 == token2

    # carrier creation
    client.post('http://127.0.0.1:8000/api/v1/carriers/',{'name':"newcarrier",'phone':"99999",'location':"here",'username':"carriernewuser",'password':"aaasssddd",'email':"carrier@trcker.com"},headers={'Authorization':'Token '+token1})
    assert Carrier.objects.get(slug='carriernewusernewmerchant').name=="newcarrier"

    #get a particular carrier details
    carrier=client.get('http://127.0.0.1:8000/api/v1/carriers/carriernewusernewmerchant',headers={'Authorization':'Token '+token1})
    assert carrier.text == '{"name":"newcarrier","phone":"99999","location":"here","email":"carrier@trcker.com","slug":"carriernewusernewmerchant"}'

    #get all carriers
    carrier=client.get('http://127.0.0.1:8000/api/v1/carriers', headers={'Authorization':'Token '+token1})
    assert carrier.text == '[{"url":"http://127.0.0.1:8000/api/v1/carriers/carriernewusernewmerchant"}]'
    
    # customer creation
    response=client.post('http://127.0.0.1:8000/api/v1/customers/',{'name':"newcustomer",'phone':"99999",'address':"here",'username':"newcustomeruser",'password':"aaasssddd",'email':"customer@trcker.com"},headers={'Authorization':'Token '+token1})
    assert Customer.objects.get(name='newcustomer').slug=="newcustomerusernewmerchant"

    #get all customers of a merchant
    customer=client.get('http://127.0.0.1:8000/api/v1/customers', headers={'Authorization':'Token '+token1})
    assert customer.text == '[{"url":"http://127.0.0.1:8000/api/v1/customers/newcustomerusernewmerchant"}]'
    
# @pytest.mark.django_db
# def test_carrier_creation(server):
#     URL = "http://127.0.0.1:8000/accounts/register/"
#     client = requests.session()
#     client.get(URL)
#     csrftoken = client.cookies['csrftoken']
#     login_data = dict(username="newuser1234",email="newuser@tracker.com",password1="aaasssddd",password2="aaasssddd",name="newmerchant",address="merchantaddress", csrfmiddlewaretoken=csrftoken)
#     r = client.post(URL, data=login_data, headers=dict(Referer=URL))
    #get a particular customer details
    customer=client.get('http://127.0.0.1:8000/api/v1/customers/newcustomerusernewmerchant',headers={'Authorization':'Token '+token1})
    assert customer.text == '{"slug":"newcustomerusernewmerchant","name":"newcustomer","phone":"99999","address":"here","merchant":2,"user":36}'
    
#     tok = client.post('http://127.0.0.1:8000/token/',{'username':"newuser1234",'password':"aaasssddd"})
#     token = Token.objects.get(user__username='newuser')
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
#     carrier=client.post('http://127.0.0.1:8000/api/v1/carrier/',{'name':"newcarrier",'phone':"99999",'location':"here",'username':"carriernewuser",'password':"aaasssddd",'email':"carrier@trcker.com"})
#     import pdb;pdb.set_trace()
    
