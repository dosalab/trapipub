from django.conf.urls import url,include
from rest_framework import routers
from tracker_api import views

router = routers.DefaultRouter()

app_name='tracker_api'

urlpatterns = [
    url(r'^log/$',views.logView.as_view({'get':'list'}), name='login'),
    url(r'^carrier/$',views.carrierView.as_view({'get':'list','post':'create'}),name='carrier'),
    url(r'^order/$',views.OrderView.as_view({'get':'list','post':'create'}),name='order'),
]

