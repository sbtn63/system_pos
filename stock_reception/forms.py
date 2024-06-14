from django import forms

from .models import StockReception
from products.models import Product
from suppliers.models import Supplier

class StockReceptionForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Seleccionar producto")
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), empty_label="Seleccionar proveedor")
    class Meta:
        model = StockReception
        fields = ['quantity_received', 'unit_price', 'reception_date', 'note', 'product', 'supplier']