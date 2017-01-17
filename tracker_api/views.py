from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Carrier,Order,Package,Merchant
from .serializer import  MerchantSerializer, CarrierSerializer, OrderSerializer, PackageSerializer, GetCarrierSerializer, CarrierUrlSerializer
from registration.views import RegistrationView
from registration.signals import user_registered
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db import transaction
from rest_framework import authentication
from django.http import HttpResponse

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
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Merchant.objects.filter(user_id=self.request.user.id)
#  /carriers/ 
class carrierView(viewsets.ModelViewSet):
    lookup_field = 'id'
    def get_serializer_class(self):
        if self.action == 'create':
            return CarrierSerializer
        if self.action == 'list':
            return CarrierUrlSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Carrier.objects.filter(merchant=self.request.user.merchant)

    def create(self, request, *args, **kwargs):
        '''carreir cretion view '''
        try:
            merchant = User.objects.get(username = self.request.user).merchant
            serializer = CarrierSerializer(data = request.data, context = {'merchant' : merchant})
            if serializer.is_valid():
                c = serializer.save()
                return (Response({"url" : c.url()}, status=status.HTTP_201_CREATED))
            else:
                return (Response(s.errors, status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant", status=status.HTTP_403_FORBIDDEN))
 
class GetCarriersView(viewsets.ModelViewSet):
    serializer_class = CarrierUrlSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Carrier.objects.filter(merchant=self.request.user.merchant)
    def get_serializer_context(self):
        return {'request':self.request}



class GetCarrierDetailsView(viewsets.ModelViewSet):
    lookup_field = 'id'   
    serializer_class = GetCarrierSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Carrier.objects.filter(merchant=self.request.user.merchant)
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        if request.data == {}:
            return (Response("Changes not given", status=status.HTTP_400_BAD_REQUEST))
        else:
            return self.update(request, *args, **kwargs)
   


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PackageView(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
