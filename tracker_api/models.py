from datetime import date
from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 

from django.core.validators import RegexValidator


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Merchant(models.Model):
    name = models.CharField(max_length=50)
    address =  models.CharField(max_length=50)
    payment_info = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE) 

class Carrier (models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    name = models.CharField(max_length=50)
    phone = models.CharField(validators=[phone_regex],max_length=15)
    location = models.CharField(max_length=20)
    merchant = models.ForeignKey('Merchant')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Carrier(id={}, name='{}')".format(self.id, repr(self.name))

    def url(self):
        return "/carriers/{}".format(self.id)

class Customer (models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    name = models.CharField(max_length=50)
    phone = models.CharField(validators=[phone_regex],max_length=15)
    address = models.CharField(max_length=20)
    merchant = models.ForeignKey('Merchant')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Carrier(id={}, name='{}')".format(self.id, repr(self.name))

    def url(self):
        return "/carriers/{}".format(self.id)

class Order(models.Model):
    merchant = models.ForeignKey('Merchant')
    customer = models.ForeignKey('Customer')
    date =  models.DateTimeField(default=date.today)
    notes = models.CharField(max_length=50)
    amount =  models.DecimalField(max_digits=10, decimal_places=2)
    invoice_number = models.CharField(max_length=20)
    
class Package (models.Model):
    orders = models.ForeignKey('Order', on_delete=models.CASCADE)
    deliverys = models.ForeignKey('Delivery', on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    date =  models.DateTimeField(default=date.today)


class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE) 
    carrier = models.ForeignKey('Carrier')
    def get_status(self):
        status = Status.objects.filter(delivery=self)
        return status

class Status(models.Model):
    delivery = models.ForeignKey('Delivery', related_name='status')
    date =  models.DateTimeField(default=date.today)
    info = models.CharField(max_length=50)
    terminal = models.BooleanField()
