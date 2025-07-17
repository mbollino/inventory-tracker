from django.db import models
from django.urls import reverse



class Product(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    sku = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_id': self.id})
    
class Order(models.Model):
    quantity_ordered = models.IntegerField()
    order_date = models.DateField()

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ordered {self.quantity_ordered()} on {self.order_date}"
