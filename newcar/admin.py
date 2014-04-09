from django.contrib import admin
from newcar.models import Maker, Car, Dealer, Buy

# Register your models here.
admin.site.register(Maker)
admin.site.register(Car)
admin.site.register(Dealer)
admin.site.register(Buy)
