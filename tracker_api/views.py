from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Carrier,Order,Merchant,Customer,Status,Delivery
from .serializer import  MerchantSerializer, CarrierSerializer, OrderSerializer, GetCarrierSerializer, CarrierUrlSerializer,CustomerSerializer,OrderUrlSerializer,orderdetailsSerializer,DeliverySerializer,DeliveryDetailsSerializer,StatusSerializer
from registration.views import RegistrationView
from registration.signals import user_registered
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.db import transaction
from rest_framework import authentication
from django.http import HttpResponse
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
        '''carrier creation '''
        try:
            merchant = User.objects.get(username = self.request.user).merchant
            serializer = CarrierSerializer(data = request.data, context = {'merchant' : merchant})
            if serializer.is_valid():
                try :
                    c = serializer.save()
                    return (Response({"url" : c.url()}, status=status.HTTP_201_CREATED))
                except:
                     return((Response("Username already exist", status=status.HTTP_409_CONFLICT)))
            else:
                return (Response(s.errors, status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant", status=status.HTTP_403_FORBIDDEN))



#  /carriers/{id} 
class GetCarrierDetailsView(viewsets.ModelViewSet):
    """ View for get the details of a specific carrier """
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

# Create a customer
class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Customer.objects.filter(merchant=self.request.user.merchant)

    def create(self, request, *args, **kwargs):
        try:
            merchant = User.objects.get(username = self.request.user).merchant
            serializer = CustomerSerializer(data = request.data, context = {'merchant' : merchant})
            if serializer.is_valid():
                c = serializer.save()
                return (Response({"url" : c.url()}, status=status.HTTP_201_CREATED))
            else:
                return (Response(s.errors, status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant", status=status.HTTP_403_FORBIDDEN))

#Create an order 
class OrderView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderSerializer
        if self.action == 'list':
            return OrderUrlSerializer
       
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Order.objects.filter(merchant=self.request.user.merchant)

    def create(self, request, *args, **kwargs):
       
        try:
            merchant = User.objects.get(username = self.request.user).merchant
            customerid = request.data['customer']
            customer = Customer.objects.get(id=customerid)
            serializer = OrderSerializer(data = request.data, context = {'merchant' : merchant,'customer':customer})
            if serializer.is_valid():
                c = serializer.save()
                return (Response(status=status.HTTP_201_CREATED))
            else:
                return (Response(s.errors, status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant", status=status.HTTP_403_FORBIDDEN))
 

# Get details of a order
class OrderDetails(viewsets.ModelViewSet):
    lookup_field = 'id'   
    serializer_class = orderdetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_queryset(self):
        return Order.objects.filter(merchant=self.request.user.merchant)

    
class DeliveryView(viewsets.ModelViewSet):
    """
    View to handle all /delivery APIs
    """
    lookup_field = 'id'
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    
    def create(self, request, *args, **kwargs):
        """
        Creates a delivery with the given params
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        newid = serializer.data['id']
        delivery = Delivery.objects.get(id=newid)
        date = datetime.datetime.now() 
        st = Status(delivery=delivery,
                       date =  date,
                       info = "Get ready",
                       terminal = False
                   )
        st.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class DeliveryDetailsView(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = DeliveryDetailsSerializer
    queryset = Delivery.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    # def retrieve(self, request, *args, **kwargs):
    #     # current_delivery=Delivery.objects.get( id=kwargs['id'])
    #     # stat=current_delivery.status_set
    #     instance = self.get_object()
    #   #  serializer = DeliveryDetailsSerializer(data = request.data, context = {'status' :stat })
    #    #  if serializer.is_valid():
           
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    

class StatusView(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
