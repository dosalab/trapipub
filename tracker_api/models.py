from datetime import date
from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 
from django.contrib.sites.models import Site
from django.core.validators import RegexValidator
from django.contrib.sites.models import Site

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Merchant(models.Model):
    name = models.CharField(max_length=50)
    address =  models.CharField(max_length=50)
    payment_info = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "<Merchant (name='{}', id={})>".format(self.name, self.id )

class Carrier (models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    name = models.CharField(max_length=50)
    phone = models.CharField(validators=[phone_regex],max_length=15)
    location = models.CharField(max_length=20)
    merchant = models.ForeignKey('Merchant')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, default='slug', primary_key=True)

    def __str__(self):
        return "Carrier(id={}, name='{}')".format(self.slug, repr(self.name))

    def url(self):
        #current_site = Site.objects.get_current()
        return "/carriers/{}".format(self.slug)

class Customer (models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    name = models.CharField(max_length=50)
    phone = models.CharField(validators=[phone_regex],max_length=15)
    address = models.CharField(max_length=20)
    merchant = models.ForeignKey('Merchant')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, default='slug', primary_key=True )


    def __str__(self):
        return "Customer(id={}, name='{}')".format(self.slug, repr(self.name))

    def url(self):
        return "/customer/{}".format(self.slug)

class Order(models.Model):
    merchant = models.ForeignKey('Merchant')
    customer = models.ForeignKey('Customer')
    date =  models.DateTimeField(default=date.today)
    notes = models.CharField(max_length=50)
    amount =  models.DecimalField(max_digits=10, decimal_places=2)
    invoice_number = models.CharField(max_length=20)
    slug = models.SlugField(max_length=50, default='slug', primary_key=True)
    def __str__(self):
        return "Order(id={}, Customer='{}')".format(self.slug, repr(self.customer))
    
    def url(self):
        return "/orders/{}".format(self.slug)

class Delivery(models.Model):
    order = models.OneToOneField('Order') 
    carrier = models.ForeignKey('Carrier')
    slug = models.SlugField(max_length=50, default='slug')
    def get_status(self):
        status = Status.objects.filter(delivery=self)
        return status
    def __str__(self):
        return "Delivery(id={})".format(self.slug)
    
    def url(self):
        return "/deliveries/{}".format(self.slug)

class Status(models.Model):
    delivery = models.ForeignKey('Delivery', related_name='status')
    date =  models.DateTimeField(default=date.today)
    info = models.CharField(max_length=50)
    terminal = models.BooleanField()

    def __str__(self):
        return "<Status(delivery='{}')>".format(self.delivery)

class TrackerSite(models.Model):
    title =  models.CharField(max_length=50)
    sites =  models.ManyToManyField(Site)

    
# class Package (models.Model):
#     orders = models.ForeignKey('Order', on_delete=models.CASCADE)
#     deliverys = models.ForeignKey('Delivery', on_delete=models.CASCADE)
#     description = models.CharField(max_length=50)
#     date =  models.DateTimeField(default=date.today)
    
# class DeliveryStage(models.Model):
#     order = models.ForeignKey('Order')
#     date =  models.DateTimeField(default=date.today)
#     info = models.CharField(max_length=50)
#     terminal = models.BooleanField()
#     location = models.CharField(max_length=50)
