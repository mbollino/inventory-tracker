from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from .models import Product, Supplier
from .forms import OrderForm, UserForm, SupplierForm, AddressForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class Home(LoginView):
    template_name = 'home.html'
    
def about(request):
    return render(request, 'about.html')

def is_zoja_user(user):
    return user.groups.filter(name__in=['ZojaViewers', 'ZojaEditors', 'ZojaUsers']).exists()

class ZojaOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.groups.filter(name__in=['ZojaViewers', 'ZojaEditors']).exists() or user.is_superuser
    
class ZojaEditorOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.groups.filter(name='ZojaEditors').exists() or user.is_superuser

@login_required
@user_passes_test(is_zoja_user)
def product_index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})

@login_required
@user_passes_test(is_zoja_user)
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    suppliers_product_doesnt_have = Supplier.objects.exclude(id__in = product.suppliers.all().values_list('id'))

    user_groups = request.user.groups.values_list('name', flat=True)
    is_editor_or_admin = not 'ZojaViewers' in user_groups

    order_form = OrderForm()

    return render(request, 'products/detail.html', {
        'product': product, 
        'order_form': order_form,
        'suppliers': suppliers_product_doesnt_have,
        'is_editor_or_admin': is_editor_or_admin
        })

class ProductCreate(LoginRequiredMixin, ZojaEditorOnlyMixin, CreateView):
    model = Product
    fields=['name', 'color', 'sku', 'quantity', 'price']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProductUpdate(LoginRequiredMixin, ZojaEditorOnlyMixin, UpdateView):
    model = Product
    fields=['name', 'color', 'sku', 'quantity', 'price']

class ProductDelete(LoginRequiredMixin, ZojaEditorOnlyMixin, DeleteView):
    model = Product
    success_url = '/products/'

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ZojaEditors').exists() or u.is_superuser)   
def add_order(request, product_id):
    form = OrderForm(request.POST)
    if form.is_valid():
        new_order = form.save(commit=False)
        new_order.product_id = product_id
        new_order.save()
    return redirect('product_detail', product_id=product_id)

class SupplierCreate(LoginRequiredMixin, ZojaEditorOnlyMixin, View):
    def get(self, request):
        supplier_form = SupplierForm()
        address_form = AddressForm()
        return render(request, 'main_app/supplier_form.html', {
            'form': supplier_form,
            'address_form': address_form
        })
    
    def post(self, request):
        supplier_form = SupplierForm(request.POST)
        address_form = AddressForm(request.POST)

        if supplier_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            supplier = supplier_form.save(commit=False)
            supplier.company_address = address
            supplier.save()
            return redirect(supplier.get_absolute_url())
        
        return render(request, 'main_app/supplier_form.html', {
            'form': supplier_form,
            'address_form': address_form
        })
    
class SupplierList(LoginRequiredMixin, ZojaOnlyMixin, ListView):
    model = Supplier
    context_object_name = 'suppliers'
    template_name = 'suppliers/supplier_index.html'

class SupplierDetail(LoginRequiredMixin, ZojaOnlyMixin, DetailView):
    model = Supplier

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = self.get_object()
        context['products'] = supplier.products.all()
            
        user_groups = self.request.user.groups.values_list('name', flat=True)
        context ['is_editor_or_admin'] = 'ZojaViewers' not in user_groups

        return context

   
class SupplierUpdate(LoginRequiredMixin, ZojaEditorOnlyMixin, UpdateView):
    def get(self, request, pk):
        supplier = self.get_object()
        supplier_form = SupplierForm(instance=supplier)
        address_instance = supplier.company_address if supplier.company_address else None
        address_form = AddressForm(instance=address_instance)
        
        return render(request, 'main_app/supplier_form.html', {
            'form': supplier_form,
            'address_form': address_form
        })
    
    def post(self, request, pk):
        supplier = self.get_object()
        address_instance = supplier.company_address if supplier.company_address else None

        supplier_form = SupplierForm(request.POST, instance = supplier)
        address_form = AddressForm(request.POST, instance=address_instance)

        if supplier_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            supplier = supplier_form.save(commit=False)
            supplier.company_address = address
            supplier.save()
            return redirect(supplier.get_absolute_url())
        
        return render(request, 'main_app/supplier_form.html', {
            'form': supplier_form,
            'address_form': address_form
        })
    
    def get_object(self):
        return Supplier.objects.get(pk=self.kwargs['pk'])

class SupplierDelete(LoginRequiredMixin, ZojaEditorOnlyMixin, DeleteView):
    model = Supplier
    success_url = '/suppliers/'

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ZojaEditors').exists() or u.is_superuser)
def associate_supplier(request, product_id, supplier_id):
    Product.objects.get(id=product_id).suppliers.add(supplier_id)
    return redirect('product_detail', product_id=product_id)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='ZojaEditors').exists() or u.is_superuser)
def remove_supplier(request, product_id, supplier_id):
    Product.objects.get(id=product_id).suppliers.remove(supplier_id)
    return redirect('product_detail', product_id=product_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserForm()
    context = {'form': form, 'error-message': error_message}
    return render(request, 'signup.html', context)