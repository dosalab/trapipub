from django.conf.urls import include,url
from django.contrib import admin
from tracker_fe import views as fe_views
from tracker_api.views import MerchantRegistration
from tracker_api.forms import MerchantRegistrationForm
from rest_framework.authtoken import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', fe_views.index, name='index'),
    url(r'^accounts/register/$', MerchantRegistration.as_view(form_class = MerchantRegistrationForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^api/v1/',include('tracker_api.urls')),
    url(r'^token/', views.obtain_auth_token,name='obtaine_token')
 
]
