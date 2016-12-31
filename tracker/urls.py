from django.conf.urls import include,url
from django.contrib import admin
from tracker_fe import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    #url(r'^tracker/', include('tracker_fe.url')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^api/v1/',include('tracker_api.urls')),
 
]
