from mapbox import Geocoder
from django.contrib.gis.geos import Point
from rest_framework.serializers import ValidationError
class Geoconverter():
    def forward(self, data):
        geocoder = Geocoder()
        response = geocoder.forward(data)
        geojson = response.geojson()
        features = geojson.get('features')
        if not features:
            raise ValidationError("Invalid address Field")
        first = response.geojson()['features'][0]
        point = first['geometry']
        latitude = point['coordinates'][0]
        longitude = point['coordinates'][1]
        point = Point(latitude, longitude)
        fullfield = {}
        fullfield["address"] = data
        fullfield["point"] = point
        return fullfield
    # def reverse(self,data):
    #     lon = data["coordinates"][0]
    #     lat = data["coordinates"][1]
    #     geocoder = Geocoder()
    #     response = geocoder.reverse(lon=lon, lat=lat)
    #     address = response.geojson()["features"][0]["place_name"]
    #     fullfield = {}
    #     fullfield["address"] = address
    #     fullfield["point"] = data
    #     return fullfield
