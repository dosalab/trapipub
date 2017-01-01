from registration.forms import RegistrationForm
from django import forms

class MerchantRegistrationForm(RegistrationForm):
    name = forms.CharField(label='name', max_length=30)
    address = forms.CharField(label='address', max_length=100)
    paymentinfo = forms.CharField(label='paymentinfo', max_length=15)
