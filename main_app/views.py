from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Product, Supplier
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
    suppliers_product_doesnt_have = Supplier.objects.exclude(id__in = product.suppliers.all().values_list('id'))
    order_form = OrderForm()
    return render(request, 'products/detail.html', {
        'product': product, 
        'order_form': order_form,
        'suppliers': suppliers_product_doesnt_have,
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

class SupplierCreate(CreateView):
    model = Supplier
    fields = '__all__'
    
class SupplierList(ListView):
    model = Supplier
    context_object_name = 'suppliers'
    template_name = 'suppliers/supplier_index.html'

class SupplierDetail(DetailView):
    model = Supplier

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = self.get_object()
        context['products'] = supplier.products.all()
        return context
   
class SupplierUpdate(UpdateView):
    model = Supplier
    fields = '__all__'

class SupplierDelete(DeleteView):
    model = Supplier
    success_url = '/suppliers/'

def associate_supplier(request, product_id, supplier_id):
    Product.objects.get(id=product_id).suppliers.add(supplier_id)
    return redirect('product_detail', product_id=product_id)

def remove_supplier(request, product_id, supplier_id):
    Product.objects.get(id=product_id).suppliers.remove(supplier_id)
    return redirect('product_detail', product_id=product_id)
