from registration.forms import RegistrationForm
from django import forms
from django.contrib.gis.forms.fields import GeometryField
class MerchantRegistrationForm(RegistrationForm):
    name = forms.CharField(label='name', max_length=30)
    address = GeometryField()
    #paymentinfo = forms.CharField(label='paymentinfo', max_length=15)
    #address = form.CharField(label='address', max_length=30)
