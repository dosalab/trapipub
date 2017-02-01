from django.contrib import admin
from .models import Merchant,Carrier,Customer,Order,Delivery,DeliveryStatus,DeliveryLog

admin.site.register(Merchant)
admin.site.register(Carrier)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(DeliveryStatus)
admin.site.register(DeliveryLog)
