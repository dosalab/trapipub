import json
from pytest import raises
from rest_framework.serializers import ValidationError
from tracker_api.customfields import ForwardField

def test_bad_name(request):
    response = ForwardField.to_internal_value(request, "kozikkod")
    assert response =="bad"

def test_currect_name(request):
    response = ForwardField.to_internal_value(request, "Calicut")
    response = response['point'].geojson
    assert '\"coordinates\": [75.955277777778, 11.136944444444]' in str(response)


# def test_repeated_names(request):
#     with raises(ValidationError) as exc:
#         ForwardField.to_representation(request, "safsaf")
#     assert "Have more points in this address" in str(exc.value)

# def test_without_name(request):
#     with raises(ValidationError) as exc:
#         ForwardField.to_representation(request, "")
#     assert "Invalid address" in str(exc.value)

# def test_proper_name(request):
#     response = ForwardField.to_representation(request, "Calicut railway station")
#     assert json.loads(response.geojson) == {"type": "Point", "coordinates": [75.781116, 11.24621]}
