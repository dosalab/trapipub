import pytest
from tracker_api.models import Carrier,Order

@pytest.mark.django_db
def test_user_count():
    assert Carrier.objects.count() == 0

@pytest.mark.django_db
def test_is_registerd():
    Carrier.objects.create(name="name",address="address",phone="12345")
    c = Carrier.objects.get(name="name")
    assert c.address == "address"

@pytest.mark.django_db
def test_order_count():
    assert Order.objects.count() == 0

@pytest.mark.django_db
def test_order_take():
    Order.objects.create(item="test_item123",price="1000",payment="COD",address="address",phone="12345")
    o = Order.objects.get(id=1)
    assert o.item == "test_item123"

