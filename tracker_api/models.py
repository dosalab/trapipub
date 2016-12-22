from django.db import models


class Carrier (models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()



# Create your models here.
