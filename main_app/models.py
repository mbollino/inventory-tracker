from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Address(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state=models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)

class Supplier(models.Model):
    company_name = models.CharField(max_length=100)
    order_link=models.URLField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    company_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.company_name
    
    def get_absolute_url(self):
        return reverse('supplier_detail', kwargs={'pk': self.id})

class Product(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    sku = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    suppliers = models.ManyToManyField(Supplier, related_name='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_id': self.id})
    
class Order(models.Model):
    quantity_ordered = models.IntegerField()
    order_date = models.DateField()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Ordered {self.quantity_ordered} on {self.order_date}"
    
    class Meta:
        ordering = ['-order_date']

    def related_suppliers(self):
        return self.product.suppliers.all()
    
    
