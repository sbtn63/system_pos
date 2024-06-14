from django import forms

from .models import StockReception

class StockReceptionForm(forms.ModelForm):
    class Meta:
        model = StockReception
        fields = ['quantity_received', 'unit_price', 'reception_date', 'note', 'product', 'supplier']