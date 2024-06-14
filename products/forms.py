from django import forms

from .models import Product
from categories.models import Category

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Seleccionar categoría")
    status = forms.ChoiceField(choices=[('', 'Seleccionar estado'),('Available', 'Disponible'), ('Disabled', 'No Disponible')])
    class Meta:
        model = Product
        fields = ['code', 'name', 'category', 'status', 'stock', 'price']

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'status', 'stock', 'price']