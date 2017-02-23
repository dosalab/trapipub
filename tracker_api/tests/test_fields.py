import json
from tracker_api.customfields import ForwardField

def test_bad_name(request):
    response = ForwardField.to_internal_value(request, "kozikkod")
    assert response == "bad"

def test_currect_name(request):
    response = ForwardField.to_internal_value(request, "Calicut")
    response = response['point'].geojson
    assert '\"coordinates\": [75.955277777778, 11.136944444444]' in str(response)
