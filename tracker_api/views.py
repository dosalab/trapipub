from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Carrier,Order,Package,Merchant
from .serializer import  MerchantSerializer,CarrierSerializer,OrderSerializer,PackageSerializer
from registration.views import RegistrationView
from registration.signals import user_registered
from django.contrib.auth import authenticate
from django.contrib.auth import login

class MerchantRegistration(RegistrationView):
    success_url = 'index'
    def register(self, form):
        data = form.cleaned_data
        username, email, password = data['username'], data['email'], data['password1']
        user=User.objects.create_user(username, email, password)
       # new_user = authenticate(username=username, password=password)
       # login(request,new_user)
       # import pdb;pdb.set_trace()
        m = Merchant(user = user)
        m.name = data['name']
        m.address = data['address']
        m.paymentinfo = data['paymentinfo']
        user = user
        m.save()
    def get_success_url(self, user):
        return 'index'


class logView(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = (permissions.IsAuthenticated)

    
class carrierView(viewsets.ModelViewSet):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    



class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PackageView(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
