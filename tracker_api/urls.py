from django.conf.urls import url,include
from rest_framework import routers
from tracker_api import views


router = routers.DefaultRouter()

app_name='tracker_api'

urlpatterns = [
    url(r'^package/$',views.PackageView.as_view({'post':'create'}),name='package'),
    url(r'^package/(?P<id>[0-9]+)/$',views.PackageView.as_view({'get':'list'}),name='packagedetail'),
    url(r'^carriers/$',views.carrierView.as_view({'post':'create','get':'list'}),name='carrier'),
    url(r'^carriers/(?P<id>[0-9]+)/?$',views.GetCarrierDetailsView.as_view({'get':'retrieve','patch':'partial_update'}), name='carrierdetail'),
    url(r'^customer/$',views.CustomerView.as_view({'post':'create','get':'list'}),name='customer'),
    url(r'^orders/$',views.OrderView.as_view({'post':'create','get' : 'list'}),name='orders'),
    url(r'^order/(?P<id>[0-9]+)/$',views.OrderDetails.as_view({'get':'retrieve','patch':'partial_update'}),name='orderdetail'),
    url(r'^deliveries/$',views.DeliveryView.as_view({'post':'create'}),name='delivery'),
]

