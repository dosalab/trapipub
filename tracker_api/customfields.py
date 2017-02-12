from rest_framework import serializers
from rest_framework.serializers import ValidationError
from mapbox import Geocoder
from django.contrib.gis.geos import Point

class ForwardField(serializers.Field):
    def to_internal_value(self, data):
        geocoder = Geocoder()
        response = geocoder.forward(data)
        geojson = response.geojson()
        features = geojson.get('features')
        if not features:
            return "bad"
            #raise ValidationError("Invalid address")
        # if len(features) > 1:
        #     raise ValidationError("Have more points in this address")
        first = response.geojson()['features'][0]
        point = first['geometry']
        latitude = point['coordinates'][0]
        longitude = point['coordinates'][1]
        point = Point(latitude, longitude)
        fullfield = {}
        fullfield["address"] = data
        fullfield["point"] = point
        return fullfield
        
    # def to_representation(self, value):
    #     # geocoder = Geocoder()
    #     # response = geocoder.forward(value)
    #     # geojson = response.geojson()
    #     # features = geojson.get('features')
    #     # if not features:
    #     #     raise ValidationError("Invalid address")
    #     # # if len(features) > 1:
    #     # #     raise ValidationError("Have more points in this address")
    #     # first = response.geojson()['features'][0]
    #     # point = first['geometry']
    #     latitude = point['coordinates'][0]
    #     longitude = point['coordinates'][1]
    #     point = Point(latitude, longitude)
    #     return point
