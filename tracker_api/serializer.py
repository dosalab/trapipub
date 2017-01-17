from django.contrib.auth.models import User
from .models import Carrier,Order,Merchant,Customer,Delivery,Status
from rest_framework import serializers
from django.db import transaction
import datetime

#Merchant details view
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

# Get details of a carrier
class GetCarrierSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    class Meta:
       model = Carrier
       fields =("id","name","phone","location", "email")


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
        

# Create an order
class OrderSerializer(serializers.Serializer):
    customer = serializers.IntegerField(required = True)
    notes = serializers.CharField(required = True)
    amount = serializers.IntegerField(required = True)
    invoice_number = serializers.IntegerField(required = True)
   
    def create(self, validated_data):
        merchant = self.context['merchant']
        customer  = self.context['customer']
        notes = validated_data['notes']
        amount = validated_data['amount']
        invoice_number = validated_data['invoice_number']
        date = datetime.datetime.now()
        with transaction.atomic():
            order = Order(merchant = merchant,
                          customer=customer ,
                          notes=notes,
                          invoice_number=invoice_number,
                          amount=amount,
                          date=date
            )
            order.save()
            return order
        
# Get all orders under a carrier
class OrderUrlSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='tracker_api:orderdetail',
        lookup_field='id'
    )
    class Meta:
        model = Order
        fields =('url',)

#get detaisl of a order
class orderdetailsSerializer(serializers.ModelSerializer):
    class Meta:
       model = Order
       fields =('__all__')


       
#create a delivery
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('__all__')

        
#status serializer
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ("__all__")


#custom related field for status
class StatusRelatedField(serializers.RelatedField):
     def to_representation(self, value):
          return {"date":value.date,"info":value.info,"terminal":value.terminal}
        
# get delivery details
class DeliveryDetailsSerializer(serializers.ModelSerializer):
    order = orderdetailsSerializer()
    carrier = GetCarrierSerializer()
    status = StatusRelatedField(many=True,read_only=True)
    # StatusSerializer(
    #     source='get_status',
    #     read_only=True
    # )
   # status = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Delivery
        fields = ('id','carrier','order','status')
