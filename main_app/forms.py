from django import forms
from .models import Order

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