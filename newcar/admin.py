from django.contrib import admin
from newcar.models import Maker, CarName, Car, Dealer, Buy

# Register your models here.
admin.site.register(Maker)
admin.site.register(CarName)
admin.site.register(Car)
admin.site.register(Dealer)
admin.site.register(Buy)
