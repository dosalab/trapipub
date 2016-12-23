from django.contrib.auth.models import User
from .models import Carrier,Order
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields =('id','name','address','phone')



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =('id','item','price','payment','address','phone')

