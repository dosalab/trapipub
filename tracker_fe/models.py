from __future__ import unicode_literals

from django.db import models

class Merchant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)

    
