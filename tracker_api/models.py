import json
from geojson import Feature, Point, FeatureCollection
from datetime import date
from django.db import models
from django.db.models import Q
from django.contrib.gis.db import models as gmodels
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 
from django.contrib.sites.models import Site
from django.core.validators import RegexValidator
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Merchant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    point = gmodels.PointField(null=True)
    payment_info = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "<Merchant (name='{}', id={})>".format(self.name, self.id )

class Carrier (models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    name = models.CharField(max_length=50)
    phone = models.CharField(validators=[phone_regex],max_length=15)
    point = gmodels.PointField(null=True)
    merchant = models.ForeignKey('Merchant')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, default='slug', primary_key=True)
    date = models.DateTimeField(default=date.today)
    @property
    def delivery(self):
        c = Q(status__name = "Assigned") | Q(status__name = "On route")
        ret = self.delivery_set.filter(c)
        if ret:
            return [x.url() for x in ret]
        else:
            return ''
     
    @property
    def deliveries(self):
        ret = self.delivery_set.all()
        if ret:
            return [x.url() for x in ret]
        else:
            return ''
           
    def __str__(self):
        return "Carrier(id={}, name='{}')".format(self.slug, repr(self.name))

    def url(self):
        return "/carriers/{}".format(self.slug)

class Customer(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    name = models.CharField(max_length=50)
    phone = models.CharField(validators=[phone_regex], max_length=15)
    address = models.CharField(max_length=150)
    point = gmodels.PointField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=50, default='slug', primary_key=True)


    def __str__(self):
        return "Customer(id={}, name='{}')".format(self.slug, repr(self.name))

    def url(self):
        return "/customers/{}".format(self.slug)

class Order(models.Model):
    merchant = models.ForeignKey('Merchant')
    customer = models.ForeignKey('Customer')
    date = models.DateTimeField(default=date.today)
    notes = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_number = models.CharField(max_length=20, unique=True)
    from_address = models.CharField(max_length=150)
    from_point = gmodels.PointField(null=True)
    to_address = models.CharField(max_length=150)
    to_point = gmodels.PointField(null=True)
    slug = models.SlugField(max_length=50, default='slug', primary_key=True)
    def __str__(self):
        return "Order(id={}, Customer='{}')".format(self.slug, repr(self.customer))
    
    def url(self):
        return "/orders/{}".format(self.slug)

class DeliveryStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Delivery(models.Model):
    order = models.OneToOneField('Order') 
    carrier = models.ForeignKey('Carrier')
    slug = models.SlugField(max_length=50, default='slug', unique=True)
    status = models.ForeignKey('DeliveryStatus')
    
    def __str__(self):
        return "Delivery(id={})".format(self.slug)
    
    def url(self):
        return "/deliveries/{}".format(self.slug)

    @property
    def progress(self):
        from_address = json.loads((self.order.from_point).geojson)
        to_address = json.loads((self.order.to_point).geojson)
        current_address = json.loads((self.carrier.point).geojson)
        from_feature = Feature(geometry=Point((from_address["coordinates"])))
        to_feature = Feature(geometry=Point((to_address["coordinates"])))
        current_feature = Feature(geometry=Point((current_address["coordinates"])))
        return FeatureCollection([from_feature, to_feature, current_feature])


class DeliveryLog(models.Model):
    delivery = models.ForeignKey('Delivery')
    date = models.DateTimeField(default=date.today)
    details = models.CharField(max_length=50)

    def __str__(self):
        return "<Status(delivery='{}')>".format(self.delivery)
