from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Carrier,Order,Merchant,Customer,Status,Delivery
from .serializer import  MerchantSerializer, CarrierSerializer, OrderSerializer, GetCarrierSerializer, CarrierUrlSerializer,CustomerSerializer,CustomerUrlSerializer,CustomerDetailsSerializer,OrderUrlSerializer,orderdetailsSerializer,DeliverySerializer,DeliveryDetailsSerializer,StatusSerializer
from registration.views import RegistrationView
from registration.signals import user_registered
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db import transaction
from rest_framework import authentication
from django.http import HttpResponse
from django.db.utils import IntegrityError
import datetime
#AS A MERCHANT
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

#  /carriers/ 
class carrierView(viewsets.ModelViewSet):
    lookup_field = 'slug'
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
        '''carrier creation '''
        try:
            merchant = User.objects.get(username = self.request.user).merchant
            serializer = CarrierSerializer(data = request.data, context = {'merchant' : merchant})
            if serializer.is_valid():
                try :
                    c = serializer.save()
#                    return (Response({"url" : c}, status=status.HTTP_201_CREATED))
                except:
                     return((Response("Username already exist", status=status.HTTP_409_CONFLICT)))
            else:
                 return (Response("Give Proper Data ", status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant", status=status.HTTP_403_FORBIDDEN))



#  /carriers/{id} 
class GetCarrierDetailsView(viewsets.ModelViewSet):
    """ View for get the details of a specific carrier """
    lookup_field = 'slug'   
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

# Create a customer
class CustomerView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerSerializer
        if self.action == 'list':
            return CustomerUrlSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Customer.objects.filter(merchant=self.request.user.merchant)

    def create(self, request, *args, **kwargs):
        try:
            merchant = User.objects.get(username = self.request.user).merchant
            serializer = CustomerSerializer(data = request.data, context = {'merchant' : merchant})
            if serializer.is_valid():
                try:
                    c = serializer.save()
                    return (Response({"url" : c.url()}, status=status.HTTP_201_CREATED))
                except IntegrityError :
                    return((Response("Username already exist", status=status.HTTP_409_CONFLICT)))
            else:
                return (Response("Give proper Data", status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant", status=status.HTTP_403_FORBIDDEN))

#  /customers/{id} 
class CustomerDetails(viewsets.ModelViewSet):
    """ View for get the details of a specific carrier """
    lookup_field = 'slug'   
    serializer_class = CustomerDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Customer.objects.filter(merchant=self.request.user.merchant)

#Create an order 
class OrderView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderSerializer
        if self.action == 'list':
            return OrderUrlSerializer

    def get_queryset(self):
        return Order.objects.filter(merchant=self.request.user.merchant)

    def create(self, request, *args, **kwargs):            
        try:
            merchant = User.objects.get(username = self.request.user).merchant
            customerid = request.data['customer']
            customer = Customer.objects.get(slug=customerid)
            serializer = OrderSerializer(data = request.data, context = {'merchant' : merchant,'customer':customer})
            if serializer.is_valid():
                order = serializer.save()
                return(Response({"url":order.url()}, status=status.HTTP_201_CREATED))
            else:
                return (Response("Give proper data", status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant", status=status.HTTP_403_FORBIDDEN))
        except Customer.DoesNotExist:
            return (Response("Wrong customer", status=status.HTTP_400_BAD_REQUEST))
        except KeyError:
             return (Response("Give Customer", status=status.HTTP_400_BAD_REQUEST))


# Get details of a order
class OrderDetails(viewsets.ModelViewSet):
    lookup_field = 'slug'   
    serializer_class = orderdetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Order.objects.filter(merchant=self.request.user.merchant)

    
class DeliveryView(viewsets.ModelViewSet):
    """
    View to handle all /delivery APIs
    """
    lookup_field = 'slug'
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def create(self, request, *args, **kwargs):
        """
        Creates a delivery with the given params
        """
        try:
            merchant = User.objects.get(username = self.request.user).merchant
            order = request.data['order']
            order = Order.objects.get(slug=order)
            carrier = request.data['carrier']
            carrier = Carrier.objects.get(slug=carrier)
            serializer = DeliverySerializer(data = request.data, context = {'order' : order,'carrier':carrier})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant", status=status.HTTP_403_FORBIDDEN))
        except IntegrityError:
            return (Response("Order already deliverd", status=status.HTTP_400_BAD_REQUEST))
        except KeyError:
            return (Response("Give proper data", status=status.HTTP_400_BAD_REQUEST))

# class DeliveryDetailsView(viewsets.ModelViewSet):
#     lookup_field = 'slug'
#     serializer_class = DeliveryDetailsSerializer
#     import pdb; pdb.set_trace()
#     queryset = Delivery.objects.get()
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (authentication.TokenAuthentication,)
    

# class StatusView(viewsets.ModelViewSet):
#     serializer_class = StatusSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (authentication.TokenAuthentication,)
