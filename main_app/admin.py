from django.contrib import admin
from .models import Product, Order, Supplier, Address

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Supplier)
admin.site.register(Address)
