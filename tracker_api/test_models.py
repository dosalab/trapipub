
from tracker_api.models import Carrier
import pytest

@pytest.mark.django_db
def test_user_count():
    assert Carrier.objects.count() == 0

@pytest.mark.django_db
def test_is_registerd():
    Carrier.objects.create(name="name",address="address",phone="12345")
    c = Carrier.objects.get(name="name")
    assert c.address == "address"

