from django import forms
from .models import Order, Supplier, Address
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity_ordered', 'order_date']
        widgets = {
            'order_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            )
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'postal_code']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'order_link', 'contact_person', 'email', 'phone_number']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']