from django import forms

from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['document', 'name', 'location', 'email', 'phone']