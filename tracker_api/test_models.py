import pytest
from tracker_api.models import Carrier,Order,Merchant
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_merchant_count():
    assert Merchant.objects.count() == 0

@pytest.mark.django_db
def test_merchant_registration():
    user=User.objects.create_user("user1","user1address", "aaasssddd")
    Merchant.objects.create(name = "merchant1", address="merchantaddress1", payment_info="cash", user=user)
    m = Merchant.objects.get(name="merchant1")
    assert m.address == "merchantaddress1"

@pytest.mark.django_db
def test_is_carrier_registerd(client):
    user=User.objects.create_user("user1","user1address", "aaasssddd")
    Merchant.objects.create(name = "merchant1", address="merchantaddress1", payment_info="cash", user=user)
    m=User.objects.get(username='user1')
    mer=m.merchant
    Carrier.objects.create(name="name",location="locationcarrier",phone="12345",merchant=mer)
    c = Carrier.objects.get(name="name")
    c=c.merchant
    assert c.name == "merchant1"

# @pytest.mark.django_db
# def test_order_count():
#     assert Order.objects.count() == 0

# @pytest.mark.django_db
# def test_order_take():
#     Order.objects.create(item="test_item123",price="1000",payment="COD",address="address",phone="12345")
#     o = Order.objects.get(id=1)
#     assert o.item == "test_item123"

 
