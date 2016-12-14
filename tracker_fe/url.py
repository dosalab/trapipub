
from django.conf.urls import url

from . import views
app_name='tracker_fe'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
