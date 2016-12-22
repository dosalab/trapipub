from django.contrib.auth.models import User
from .models import Carrier
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')
class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields =('id','name','address','phone')
