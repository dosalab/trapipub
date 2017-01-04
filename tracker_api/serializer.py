#from django.contrib.auth.models import User
from .models import Carrier,Order,Package,Merchant
from rest_framework import serializers

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('name', 'address', 'payment_info','user')


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields =('name', 'phone', 'location' )

        #fields =('name', 'phone', 'location', 'merchants', 'deliverise' )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =('id','date','notes','amount',)


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields =('id','description')

