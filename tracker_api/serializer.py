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
                              point=location['point'],
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
        fields = ("name", "phone","point", "email", "delivery")

# Update details of a carrier
class PatchCarrier(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = ("name", "phone","point","date")

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

# Get deliveries of a carrier
class CarrierDeliveries(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = ("deliveries",)

        
# create a customer
class CustomerSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    phone = serializers.IntegerField(required=True)
    address = ForwardField(required=True)
    def validate_address(self, value):
        if value == "bad":
            raise ValidationError("Invalid address")
        return value

    def create(self, validated_data):
        name = validated_data['name']
        phone = validated_data['phone']
        address = validated_data.get('address')
        with transaction.atomic():
            cus = Customer(name=name,
                           phone=phone,
                           address=address['address'],
                           point=address['point'])
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
        fields = ('name', 'phone', 'address','point')

# Get details of a customer
class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('user',)

# Create an order
class OrderSerializer(serializers.Serializer):
    customer = serializers.CharField(required=True)
    notes = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)
    invoice_number = serializers.CharField(required=True)
    from_address = ForwardField(required=True)
    to_address = ForwardField(required=True)
    def validate_to_address(self, value):
        if value == "bad":
            raise ValidationError("Invalid address")
        return value
    def validate_from_address(self, value):
        if value == "bad":
            raise ValidationError("Invalid address")
        return value

    def create(self, validated_data):
        merchant = self.context['merchant']
        customer = self.context['customer']
        notes = validated_data['notes']
        amount = validated_data['amount']
        invoice_number = validated_data['invoice_number']
        date = datetime.datetime.now()
        from_address = validated_data.get('from_address')
        to_address = validated_data.get('to_address')
        with transaction.atomic():
            order = Order(merchant=merchant,
                          customer=customer,
                          notes=notes,
                          invoice_number=invoice_number,
                          amount=amount,
                          date=date,
                          from_address=from_address["address"],
                          from_point=from_address["point"],
                          to_address=to_address["address"],
                          to_point=to_address["point"])
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

#get details of a order
class orderdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('invoice_number', 'date', 'amount', 'customer', 'notes',"from_address","from_point","to_address","to_point")

#Patch details of a order
class OrderPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('invoice_number', 'date', 'amount', 'notes',"from_address","to_address")


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


#custom related field for status
class StatusRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

class DeliveryDetails(serializers.ModelSerializer):
    order = OrderUrlSerializer()
    from_address =GeometryField(source='order.from_point')
    to_address  = GeometryField(source='order.to_point')
    carrier = CarrierUrlSerializer()
    status = StatusRelatedField(read_only=True)
    customer = serializers.CharField(source='order.customer.slug')
    current_location = GeometryField(source='carrier.point')
    last_updated = serializers.DateTimeField(source='carrier.date')
    progress = GeometryField()

    class Meta:
        model = Delivery
        fields = ('progress','order','carrier','customer','status','last_updated','from_address','to_address','current_location')
    
class DeliveryUrls(serializers.HyperlinkedModelSerializer):
    url = CustomHyperlink(
        view_name='tracker_api:deliverydetails',
        lookup_field='slug'
    )
    class Meta:
        model = Delivery
        fields = ("url",)

class DeliverystatusUrls(serializers.HyperlinkedModelSerializer):
    url = CustomHyperlink(
        view_name='tracker_api:deliverydetails',
        lookup_field='slug'
    )
    status = StatusRelatedField(read_only=True)
    class Meta:
        model = Delivery
        fields = ("url",'status')


class CarrierDeliveryStatusSerilaizer(serializers.HyperlinkedModelSerializer):
    delivery = CustomHyperlink(
        view_name='tracker_api:deliverydetails',
        lookup_field='slug'
    )
    order =CustomHyperlink(
        view_name='tracker_api:orderdetail',
        lookup_field='slug'
    ) 
    status = StatusRelatedField(read_only=True)
    location = serializers.CharField(source='carrier.point')
    class Meta:
        model = Delivery
        fields = ("order","delivery",'status','location')

# Create a delivery
class  CarrierDeliveryOrderSeriliazer(serializers.Serializer):
    order = serializers.CharField(required=True)
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


# Get details of a customer
class CustomerOrderDetailsSerializer(serializers.ModelSerializer):
   # order = OrderUrlSerializer()
    class Meta:
        model = Customer
        fields = ('name', 'phone', 'address','point','order_set')
 
#Change password
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
