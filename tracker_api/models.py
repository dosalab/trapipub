from datetime import date
from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Merchant(models.Model):
    name = models.CharField(max_length=50)
    address =  models.CharField(max_length=50)
    payment_info = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Carrier (models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    location = models.CharField(max_length=20)
    merchant = models.ForeignKey('Merchant')

    def __repr__(self):
        return "<Carrier(name={})>".format(repr(self.name))

    
class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=30)
    phone = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Carrier (models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    location = models.CharField(max_length=20)
    merchants = models.ForeignKey('Merchant')
    deliverise = models.ForeignKey('Delivery', null=True)



class Order (models.Model):
    merchants = models.ForeignKey('Merchant')
    customer = models.ForeignKey('Customer')
    packages = models.ForeignKey('Package', on_delete=models.CASCADE)
    status = models.ForeignKey('Orderstatus', on_delete=models.CASCADE)
    date =  models.DateTimeField(default=date.today)
    notes = models.CharField(max_length=50)
    amount =  models.DecimalField(max_digits=10, decimal_places=2)
    invoicenumber = models.CharField(max_length=20)
    deliveryaddress = models.CharField(max_length=200)
    

class Orderstatus(models.Model):
    status = models.CharField(max_length=20)
    date =  models.DateTimeField(default=date.today)
    info = models.CharField(max_length=50)
    terminal = models.BooleanField()
    
class Package (models.Model):
    orders = models.ForeignKey('Order', on_delete=models.CASCADE)
    deliverys = models.ForeignKey('Delivery', on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    date =  models.DateTimeField(default=date.today)


class Delivery(models.Model):
    packages = models.ForeignKey('Package', on_delete=models.CASCADE)
    carriers = models.ForeignKey('Carrier') 
    status = models.ForeignKey('Deliverystage', on_delete=models.CASCADE)


class Deliverystage(models.Model):
    order = models.ForeignKey('Order')
    date =  models.DateTimeField(default=date.today)
    info = models.CharField(max_length=50)
    terminal = models.BooleanField()
    location = models.CharField(max_length=50)
