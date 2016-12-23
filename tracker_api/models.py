from datetime import date

from django.db import models


class Carrier (models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()


class Order (models.Model):
    item = models.CharField(max_length=200)
    time =  models.DateTimeField(default=date.today)
    price =  models.DecimalField(max_digits=10, decimal_places=2)
    payment =  models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()
