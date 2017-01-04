from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Carrier,Order,Package,Merchant
from .serializer import  MerchantSerializer, CarrierSerializer, OrderSerializer, PackageSerializer
from registration.views import RegistrationView
from registration.signals import user_registered
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db import transaction


class MerchantRegistration(RegistrationView):

    def register(self, form):
        data = form.cleaned_data
        username, email, password = data['username'], data['email'], data['password1']
        with transaction.atomic():
            user=User.objects.create_user(username, email, password)
            m = Merchant(user = user)
            m.name = data['name']
            m.address = data['address']
            m.save()

    def get_success_url(self, user):
        return 'index'


class logView(viewsets.ModelViewSet):
    serializer_class = MerchantSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return Merchant.objects.filter(user_id=self.request.user.id)

class carrierView(viewsets.ModelViewSet):
    lookup_field = 'id'   
    serializer_class = CarrierSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return Carrier.objects.filter(merchant=self.request.user.merchant)


    def create(self, request, *args, **kwargs):
        request.data['user_id'] = request.user.id
        return super(self.__class__, self).create(request, *args, **kwargs)




class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PackageView(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
