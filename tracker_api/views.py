import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from registration.views import RegistrationView
#from registration.signals import user_registered
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import authentication
from django.http import HttpResponse
#from django.contrib.auth import login
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token
#from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from .models import Carrier, Order, Merchant, Customer, Delivery, DeliveryStatus,DeliveryLog
from .serializer import  CarrierSerializer, OrderSerializer, GetCarrierSerializer, CarrierUrlSerializer, PatchCarrier, CustomerSerializer,CustomerUrlSerializer,CustomerDetailsSerializer,OrderUrlSerializer,orderdetailsSerializer,DeliverySerializer,CarrierDeliveries,DeliveryUrls,DeliveryDetails,DeliverystatusUrls,CarrierDeliveryStatusSerilaizer, CarrierDeliveryOrderSeriliazer,CustomerOrderDetailsSerializer,CustomerRegisterSerializer,ChangePasswordSerializer, OrderPatchSerializer
from tracker_api.helpers import Geoconverter
#AS A MERCHANT
class MerchantRegistration(RegistrationView):
    def register(self, form):
        data = form.cleaned_data
        username = data['username']
        email = data['email']
        password = data['password1']
        resp = Geoconverter.forward(self, data["address"])
        with transaction.atomic():
            user = User.objects.create_user(username, email, password)
            merchant = Merchant(user=user)
            merchant.name = data['name']
            merchant.address = data['address']
            merchant.point = resp["point"]
            merchant.save()

    def get_success_url(self, user):
        return 'index'

#/carriers/
class carrierView(viewsets.ModelViewSet):
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CarrierUrlSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        '''carrier creation '''
        try:
            merchant = User.objects.get(username=self.request.user).merchant
            queryset = Carrier.objects.filter(merchant=self.request.user.merchant)
            serializer = CarrierSerializer(data=request.data,
                                           context={'merchant' : merchant})
            if serializer.is_valid():
                try:
                    carrier = serializer.save()
                    sitename = get_current_site(request).domain
                    return (Response({"url" :'http://{}/api/v1{}'.format(sitename, carrier.url())},
                                     status=status.HTTP_201_CREATED))
                except IntegrityError:
                    return((Response("Username already exist",
                                     status=status.HTTP_409_CONFLICT)))
            else:
                return (Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))

    def list(self, request, *args, **kwargs):
        try:
            queryset = Carrier.objects.filter(merchant=self.request.user.merchant)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))


#/carriers/{id}
class GetCarrierDetailsView(viewsets.ModelViewSet):
    """ View for get the details of a specific carrier """
    lookup_field = 'slug'
    queryset = Carrier.objects.all()
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GetCarrierSerializer
        if self.action == 'partial_update':
            return PatchCarrier
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        try:
            if  User.objects.get(username =self.request.user).merchant == Carrier.objects.get(slug=kwargs["slug"]).merchant:
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response("Its not your carrier",status=status.HTTP_400_BAD_REQUEST)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))

    def partial_update(self, request, *args, **kwargs):
        try:
            if User.objects.get(username=self.request.user).carrier == Carrier.objects.get(slug=kwargs["slug"]):
                kwargs['partial'] = True
                if request.data == {}:
                    return (Response("Changes not given", status=status.HTTP_400_BAD_REQUEST))
                elif request.data.get("point"):
                    request.data["date"] = datetime.datetime.now()
                    return self.update(request, *args, **kwargs)
                else:
                    return self.update(request, *args, **kwargs)
            else:
                return Response("Its not your id",status=status.HTTP_400_BAD_REQUEST)
        except User.carrier.RelatedObjectDoesNotExist:
            return (Response("User is not a carrier",
                             status=status.HTTP_403_FORBIDDEN))
                    elif request.data.get("point"):
                        request.data["date"] = datetime.datetime.now()
                        return self.update(request, *args, **kwargs)

#/carriers/{id}/deliveries
class CarrierDeliveryView(viewsets.ModelViewSet):
    """ View for get the deliveries of a specific carrier """
    lookup_field = 'slug'
    queryset = Carrier.objects.all()
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return  CarrierDeliveries
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def create(self, request, *args, **kwargs):
        """
        Creates a delivery with the given order
        """
        try:
            if  User.objects.get(username =self.request.user).merchant == Carrier.objects.get(slug=kwargs["slug"]).merchant:
                order = Order.objects.get(slug=request.data['order'])
                carrier = Carrier.objects.get(slug=kwargs["slug"])
                stat = DeliveryStatus.objects.get(name="Assigned")
                serializer =  CarrierDeliveryOrderSeriliazer(data=request.data,
                                                             context = {'order' : order, 'carrier':carrier, 'stat':stat})
                if serializer.is_valid():
                    delivery = serializer.save()
                    sitename = get_current_site(request).domain
                    return (Response({"url" :'http://{}/api/v1{}'.format(sitename,delivery.url())},
                                     status=status.HTTP_201_CREATED))
                else: 
                    return (Response(serializer.errors,
                                     status=status.HTTP_400_BAD_REQUEST))
            else:
                return Response("Its not your carrier",status=status.HTTP_400_BAD_REQUEST)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))
        except IntegrityError:
            return (Response("Order already deliverd",
                             status=status.HTTP_400_BAD_REQUEST))
        except Carrier.DoesNotExist:
            return (Response("Give proper Carrier",
                             status=status.HTTP_400_BAD_REQUEST))
        except Order.DoesNotExist:
            return (Response("Give proper Order",
                             status=status.HTTP_400_BAD_REQUEST))
        except KeyError:
            return (Response("Give proper data",
                             status=status.HTTP_400_BAD_REQUEST))
   
    def retrieve(self, request, *args, **kwargs):
        try:
            if  User.objects.get(username =self.request.user).merchant == Carrier.objects.get(slug=kwargs["slug"]).merchant:
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response("Its not your carrier",status=status.HTTP_400_BAD_REQUEST)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))

class CarrierDeliveryStatusView(viewsets.ModelViewSet):
    """ View for get the deliveries of a specific carrier """
    lookup_field = 'slug'
    queryset = Carrier.objects.all()
    def get_serializer_class(self):
        if self.action == 'list':
          return  CarrierDeliveryStatusSerilaizer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def list(self, request, *args, **kwargs):
        carrier = Carrier.objects.get(slug=kwargs['slug'])
        queryset = Delivery.objects.filter(Q(order__merchant=self.request.user.merchant),Q(status__name=kwargs["status"]),Q(carrier=carrier))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

        
# Create a customer
class CustomerView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerSerializer
        if self.action == 'list':
            return CustomerUrlSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def create(self, request, *args, **kwargs):
        try:
            User.objects.get(username=self.request.user).merchant
            queryset = Customer.objects.all()
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    customer = serializer.save()
                    sitename = get_current_site(request).domain
                    return (Response({"url" :'http://{}/api/v1{}'.format(sitename, customer.url())},
                                     status=status.HTTP_201_CREATED))
                except IntegrityError:
                    return((Response("Username already exist",
                                     status=status.HTTP_409_CONFLICT)))
            else:
                return (Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))

    def list(self, request, *args, **kwargs):
        try:
            queryset = Customer.objects.filter(order__merchant=self.request.user.merchant).distinct()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))

#/customers/{id} 
class CustomerDetails(viewsets.ModelViewSet):
    """ View for get the details of a specific carrier """
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Customer.objects.all()
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return CustomerDetailsSerializer
    def retrieve(self, request, *args, **kwargs):
        try:
            User.objects.get(username=self.request.user).merchant
            instance = self.get_object()
            serializer = CustomerDetailsSerializer(instance)
            return Response(serializer.data)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))

    def partial_update(self, request, *args, **kwargs):
        try:
            User.objects.get(username=self.request.user).merchant
            kwargs['partial'] = True
            if request.data == {}:
                return (Response("Changes not given",
                                 status=status.HTTP_400_BAD_REQUEST))
            else:
                return self.update(request, *args, **kwargs)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))

class CustomerRegister(viewsets.ModelViewSet):
    """ View for get the details of a specific carrier """
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Customer.objects.all()
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return CustomerRegisterSerializer
    def partial_update(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(slug=kwargs["slug"])
            User.objects.get(username=self.request.user).merchant
            kwargs['partial'] = True
            if request.data == {}:
                try:
                    user = User.objects.create_user(customer.phone,"null",customer.name)
                    request.data._mutable = True
                    request.data["user"]=user.pk
                    request.data._mutable = False
                except IntegrityError:
                     return (Response("Customer already registerd",
                                      status=status.HTTP_403_FORBIDDEN))
            else:
                user = User.objects.create_user(customer.phone,request.data["email"],customer.name)
                request.data["user"]=user.pk
            return self.update(request, *args, **kwargs)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))


class CustomerOrderDetails(viewsets.ModelViewSet):
    """ View for get the details of customer with their orders """
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Customer.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        try:
            User.objects.get(username=self.request.user).merchant
            instance = self.get_object()
            serializer = CustomerOrderDetailsSerializer(instance)
            return Response(serializer.data)
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))
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
            merchant = User.objects.get(username=self.request.user).merchant
            customerid = request.data['customer']
            customer = Customer.objects.get(slug=customerid)
            serializer = OrderSerializer(data=request.data,
                                         context={'merchant' : merchant,
                                                  'customer':customer})
            if serializer.is_valid():
                order = serializer.save()
                sitename = get_current_site(request).domain
                return (Response({"url" :'http://{}/api/v1{}'.format(sitename, order.url())},
                                 status=status.HTTP_201_CREATED))
            else:
                return (Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST))
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))
        except Customer.DoesNotExist:
            return (Response("Wrong customer",
                             status=status.HTTP_400_BAD_REQUEST))
        except KeyError:
             return (Response("Give Customer",
                              status=status.HTTP_400_BAD_REQUEST))
   
# Get details of a order
class OrderDetails(viewsets.ModelViewSet):
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return orderdetailsSerializer
        if self.action == 'partial_update':
            return OrderPatchSerializer
    def get_queryset(self):
        return Order.objects.filter(merchant=self.request.user.merchant)


class DeliveryView(viewsets.ModelViewSet):
    """
    View to handle all /delivery APIs
    """
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'create':
            return DeliverySerializer
        if self.action == 'list':
            return DeliveryUrls


    def create(self, request, *args, **kwargs):
        """
        Creates a delivery with the given params
        """
        try:
            User.objects.get(username=self.request.user).merchant
            order = Order.objects.get(slug=request.data['order'])
            carrier = Carrier.objects.get(slug=request.data['carrier'])
            stat = DeliveryStatus.objects.get(name="Assigned")
            serializer = DeliverySerializer(data=request.data,
                                            context = {'order' : order, 'carrier':carrier, 'stat':stat})
            if serializer.is_valid():
                delivery = serializer.save()
                sitename = get_current_site(request).domain
                return (Response({"url" :'http://{}/api/v1{}'.format(sitename,delivery.url())},
                                 status=status.HTTP_201_CREATED))
            else: 
                return (Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST))
                
        except User.merchant.RelatedObjectDoesNotExist:
            return (Response("User is not a merchant",
                             status=status.HTTP_403_FORBIDDEN))
        except IntegrityError:
            return (Response("Order already deliverd",
                             status=status.HTTP_400_BAD_REQUEST))
        except Carrier.DoesNotExist:
            return (Response("Give proper Carrier",
                             status=status.HTTP_400_BAD_REQUEST))
        except Order.DoesNotExist:
            return (Response("Give proper Order",
                             status=status.HTTP_400_BAD_REQUEST))
        except KeyError:
            return (Response("Give proper data",
                             status=status.HTTP_400_BAD_REQUEST))
        
    def list(self, request, *args, **kwargs):
        queryset = Delivery.objects.filter(order__merchant=self.request.user.merchant)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




class DeliveryStatusView(viewsets.ModelViewSet):
    """
    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'list':
            return DeliverystatusUrls
    
    def list(self, request, *args, **kwargs):
        queryset = Delivery.objects.filter(Q(order__merchant=self.request.user.merchant),Q(status__name=kwargs["status"]) )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
class DeliveryDetailsView(viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = DeliveryDetails
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def get_queryset(self):
        return Delivery.objects.filter(order__merchant=self.request.user.merchant)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# class StatusView(viewsets.ModelViewSet):
#     serializer_class = StatusSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (authentication.TokenAuthentication,)


##PASSWORD CHANGE

class ChangePasswordView(viewsets.ModelViewSet):
    """
    A view  for changing password.
  """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        queryset = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not queryset.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset.set_password(serializer.data.get("new_password"))
            queryset.save()
            Token.objects.get(user_id=request.user.id).delete()
            Token.objects.create(user_id=request.user.id)
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
