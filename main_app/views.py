from django.shortcuts import render
from .models import Product

def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

def product_index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})
    

