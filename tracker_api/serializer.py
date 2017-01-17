from django.contrib.auth.models import User
from .models import Carrier,Order,Merchant,Customer,Delivery,Status
from rest_framework import serializers
from django.db import transaction

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('name', 'address', 'payment_info','user')

#Carrier creation 
class CarrierSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    phone = serializers.IntegerField(required = True)
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    location = serializers.CharField(required = False,default="")
    def create(self, validated_data):

        merchant = self.context['merchant']
        name  = validated_data['name']
        phone = validated_data['phone']
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        location = validated_data['location']

        with transaction.atomic():
            u = User.objects.create_user(username, email, password)
            c = Carrier(name = name,
                        phone = phone,
                        location = location,
                        merchant = merchant,
                        user = u)
            c.save()
            return c




class GetCarrierSerializer(serializers.ModelSerializer):
 #  merchant = MerchantSerializer()
    class Meta:
       model = Carrier
       fields =("id","name","phone","location")


#Get all carriers urls under a merchant
class CarrierUrlSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='tracker_api:carrierdetail',
        lookup_field='id'
    )
    class Meta:
        model = Carrier
        fields =("url",)

# create a customer
class CustomerSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    phone = serializers.IntegerField(required = True)
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    address = serializers.CharField(required = True)
   
    def create(self, validated_data):
        merchant = self.context['merchant']
        name  = validated_data['name']
        phone = validated_data['phone']
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        address = validated_data['address']
        with transaction.atomic():
            usr = User.objects.create_user(username, email, password)
            c = Customer(name = name,
                        phone = phone,
                        address = address,
                        merchant = merchant,
                         user = usr)
            c.save()
            return c
        
    class Meta:
        model = Order
        fields =('id','date','notes','amount',)


       
    class Meta:
        model = Package
        fields =('id','description')

