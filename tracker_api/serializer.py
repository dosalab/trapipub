from django.contrib.auth.models import User
from .models import Carrier,Order,Package,Merchant
from rest_framework import serializers

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('name', 'address', 'payment_info','user')

      
class CarrierSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    phone = serializers.IntegerField(required = True)
    location = serializers.CharField(required = False, allow_blank = True)
    # merchant = serializers.PrimaryKeyRelatedField(required=False,
    #                                               read_only = True,
    #                                               default=serializers.CurrentUserDefault().merchant)

    def create(self, validated_data):
        merchant = User.objects.get(username = self.context['request'].user).merchant
        name = validated_data['name']
        phone = validated_data['phone']
        location = validated_data.get('location', '')
        m = Carrier(name = name,
                    phone = phone,
                    location = location,
                    merchant = merchant)
        m.save()
        return m


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields =('id','date','notes','amount',)


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields =('id','description')

