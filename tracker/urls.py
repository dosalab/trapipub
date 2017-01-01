from django.conf.urls import include,url
from django.contrib import admin
from tracker_fe import views
from tracker_api.views import MerchantRegistration
from tracker_api.forms import MerchantRegistrationForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^accounts/register/$', MerchantRegistration.as_view(form_class = MerchantRegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^api/v1/',include('tracker_api.urls')),
 
]
