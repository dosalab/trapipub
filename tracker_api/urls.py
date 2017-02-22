from django.conf.urls import url,include
from rest_framework import routers
from tracker_api import views


router = routers.DefaultRouter()

app_name='tracker_api'

urlpatterns = [
    url(r'^changepwd$',views.ChangePasswordView.as_view({'patch':'partial_update'}),name='change_password'),
    url(r'^carriers$',views.carrierView.as_view({'post':'create','get':'list'}),name='carrier'),
    url(r'^carriers/(?P<slug>[-\w]+)$',views.GetCarrierDetailsView.as_view({'get':'retrieve','patch':'partial_update'}), name='carrierdetail'),
    url(r'^carriers/(?P<slug>[-\w]+)/deliveries$',views.CarrierDeliveryView.as_view({'post':'create','get':'retrieve'}), name='carrierdeliveries'),
    url(r'^carriers/(?P<slug>[-\w]+)/deliveries/(?:status=(?P<status>[-\w+]+))$',views.CarrierDeliveryStatusView.as_view({'get':'list'}), name='carrierdeliveries'),
    url(r'^customers/?$',views.CustomerView.as_view({'post':'create','get':'list'}),name='customer'),
    url(r'^customers/(?P<slug>[-\w]+)$',views.CustomerDetails.as_view({'get':'retrieve','patch':'partial_update'}), name='customerdetails'),
    url(r'^customers/(?P<slug>[-\w]+)/orders$',views.CustomerOrderDetails.as_view({'get':'retrieve'}), name='customeroderdetails'),
    url(r'^orders$',views.OrderView.as_view({'post':'create','get' : 'list'}),name='orders'),
    url(r'^orders/(?P<slug>[-\w]+)/?$',views.OrderDetails.as_view({'get':'retrieve','patch':'partial_update'}),name='orderdetail'),
    url(r'^deliveries$',views.DeliveryView.as_view({'post':'create','get':'list'}),name='delivery'),
    url(r'^deliveries/(?:status=(?P<status>[-\w+]+))$',views.DeliveryStatusView.as_view({'get':'list'}),name='deliverystatus'),
    url(r'^deliveries/(?P<slug>[-\w+]+)$',views.DeliveryDetailsView.as_view({'get':'retrieve','patch':'partial_update'}), name='deliverydetails'),
]
