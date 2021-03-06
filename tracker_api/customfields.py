from rest_framework import serializers
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
        first = response.geojson()['features'][0]
        point = first['geometry']
        latitude = point['coordinates'][0]
        longitude = point['coordinates'][1]
        point = Point(latitude, longitude)
        fullfield = {}
        fullfield["address"] = data
        fullfield["point"] = point
        return fullfield
