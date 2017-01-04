from django.conf.urls import url,include
from rest_framework import routers
from tracker_api import views

router = routers.DefaultRouter()

app_name='tracker_api'

urlpatterns = [
    url(r'^log/$',views.logView.as_view({'get':'list'}), name='login'),
    url(r'^carrier/$',views.carrierView.as_view({'post':'create','get':'list'}),name='carrier'),
    url(r'^carrier/(?P<id>[0-9]+)/?$',views.carrierView.as_view({'get':'retrieve'}), name='carrierdetail'),
    url(r'^order/$',views.OrderView.as_view({'post':'create'}),name='order'),
    url(r'^order/(?P<id>[0-9]+)/$',views.OrderView.as_view({'get':'list'}),name='orderdetail'),
    url(r'^package/$',views.PackageView.as_view({'post':'create'}),name='package'),
    url(r'^package/(?P<id>[0-9]+)/$',views.PackageView.as_view({'get':'list'}),name='packagedetail'),
]

