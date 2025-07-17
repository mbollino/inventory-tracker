from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product

def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

def product_index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/detail.html', {'product': product})

class ProductCreate(CreateView):
    model = Product
    fields=['name', 'color', 'sku', 'quantity', 'price']

class ProductUpdate(UpdateView):
    model = Product
    fields=['name', 'color', 'sku', 'quantity', 'price']

class ProductDelete(DeleteView):
    model = Product
    success_url = '/products/'
   
    

