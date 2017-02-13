import datetime
from rest_framework.serializers import ValidationError
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_gis.fields import GeometryField
from .models import Carrier, Order, Merchant, Customer, Delivery, DeliveryStatus,DeliveryLog
from tracker_api.customfields import ForwardField

#Merchant details view
class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('name', 'address', 'payment_info', 'user')

#Carrier creation 
class CarrierSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    phone = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    location = ForwardField(required=True)
    def validate_location(self, value):
        if value == "bad":
            raise ValidationError("Invalid address")
        return value

    def create(self, validated_data):
        merchant = self.context['merchant']
        name = validated_data['name']
        phone = validated_data['phone']
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        location = validated_data.get('location')
        with transaction.atomic():
            user = User.objects.create_user(username, email, password)
            carrier = Carrier(name=name,
                              phone=phone,
                              location=location['address'],
                              locationpoint=location['point'],
                              merchant=merchant,
                              user=user)
            carrier.slug = slugify(user.username+merchant.name)
            carrier.save()
            return carrier

# Get details of a carrier
class GetCarrierSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = Carrier
        fields = ("name", "phone", "location","locationpoint", "email", "delivery")

# Update details of a carrier
class PatchCarrier(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = ("name", "phone", "location","locationpoint")

class CustomHyperlink(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'slug': obj.slug,
        }
        return 'http://{}{}'.format(get_current_site(request),
                                    reverse(view_name, kwargs=url_kwargs))

#Get all carriers urls under a merchant
class CarrierUrlSerializer(serializers.HyperlinkedModelSerializer):
    url = CustomHyperlink(
        view_name='tracker_api:carrierdetail',
        lookup_field='slug'
    )
    class Meta:
        model = Carrier
        fields = ("url",)

# create a customer
class CustomerSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    phone = serializers.IntegerField(required=True)
    #username = serializers.CharField(required=True)
    #password = serializers.CharField(required=True)
    #email = serializers.EmailField(required=True)
    address = GeometryField(required=False)

    def create(self, validated_data):
        name = validated_data['name']
        phone = validated_data['phone']
        address = validated_data.get('address')
        with transaction.atomic():
            cus = Customer(name=name,
                           phone=phone,
                           address=address)
            cus.slug = slugify(cus.phone)
            cus.save()
            return cus

# Get all orders under a carrier
class CustomerUrlSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='tracker_api:customerdetails',
        lookup_field='slug'
    )
    class Meta:
        model = Customer
        fields = ('url',)

# Get details of a customer
class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'phone', 'address')

# Create an order
class OrderSerializer(serializers.Serializer):
    customer = serializers.CharField(required=True)
    notes = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)
    invoice_number = serializers.CharField(required=True)

    def create(self, validated_data):
        merchant = self.context['merchant']
        customer = self.context['customer']
        notes = validated_data['notes']
        amount = validated_data['amount']
        invoice_number = validated_data['invoice_number']
        date = datetime.datetime.now()
        with transaction.atomic():
            order = Order(merchant=merchant,
                          customer=customer,
                          notes=notes,
                          invoice_number=invoice_number,
                          amount=amount,
                          date=date)
            order.slug = slugify(invoice_number)
            order.save()
            return order

# Get all orders under a carrier
class OrderUrlSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='tracker_api:orderdetail',
        lookup_field='slug')
    class Meta:
        model = Order
        fields = ('url',)

#get detaisl of a order
class orderdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('invoice_number', 'date', 'amount', 'customer', 'notes')


# Create a delivery
class DeliverySerializer(serializers.Serializer):
    order = serializers.CharField(required=True)
    carrier = serializers.CharField(required=True)
    def create(self, validated_data):
        order = self.context['order']
        carrier = self.context['carrier']
        stat = self.context['stat']
        delivery = Delivery(order=order,
                            carrier=carrier,
                            status=stat)
        delivery.slug = slugify(order.slug+carrier.name)
        with transaction.atomic():
            delivery.save()
            delivery = Delivery.objects.get(slug=delivery.slug)
            date = datetime.datetime.now()
            dlog = DeliveryLog(delivery=delivery,
                               date=date,
                               details="Get ready")
            dlog.save()
        return delivery

#status serializer
class DeliveryStatus(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = ("__all__")


# #custom related field for status
# class StatusRelatedField(serializers.RelatedField):
#     def to_representation(self, value):
#         return {"date":value.date,
#                 "info":value.info,
#                 "terminal":value.terminal}
        
# # get delivery details
# class DeliveryDetails(serializers.ModelSerializer):
#     # order = orderdetailsSerializer()
#     # carrier = GetCarrierSerializer()
#     status = StatusRelatedField(many=True, read_only=True)
#     class Meta:
#         model = Delivery
#         fields = ('id', 'carrier', 'order', 'status')
    
