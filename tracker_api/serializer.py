from django.contrib.auth.models import User
from .models import Carrier,Order,Package,Merchant
from rest_framework import serializers
from django.db import transaction

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('name', 'address', 'payment_info','user')

      
class CarrierSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    phone = serializers.IntegerField(required = True)
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)

    def create(self, validated_data):

        merchant = self.context['merchant']
        name  = validated_data['name']
        phone = validated_data['phone']
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']

        with transaction.atomic():
            u = User.objects.create_user(username, email, password)
            c = Carrier(name = name,
                        phone = phone,
                        location = '',
                        merchant = merchant,
                        user = u)
            c.save()
            return c




class GetCarrierSerializer(serializers.ModelSerializer):
 #  merchant = MerchantSerializer()
    class Meta:
       model = Carrier
       fields =("id","name","phone","location")

class CarrierUrlSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='tracker_api:carrierdetail',
        lookup_field='id'
    )
    class Meta:
        model = Carrier
        fields =("url",)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =('id','date','notes','amount',)


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields =('id','description')

