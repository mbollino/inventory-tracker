from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Product
from .forms import OrderForm

def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

def product_index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    order_form = OrderForm()
    return render(request, 'products/detail.html', {
        'product': product, 'order_form': order_form
        })

class ProductCreate(CreateView):
    model = Product
    fields=['name', 'color', 'sku', 'quantity', 'price']

class ProductUpdate(UpdateView):
    model = Product
    fields=['name', 'color', 'sku', 'quantity', 'price']

class ProductDelete(DeleteView):
    model = Product
    success_url = '/products/'
   
def add_order(request, product_id):
    form = OrderForm(request.POST)
    if form.is_valid():
        new_order = form.save(commit=False)
        new_order.product_id = product_id
        new_order.save()
    return redirect('product_detail', product_id=product_id)
    

