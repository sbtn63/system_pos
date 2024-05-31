from django import forms

from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['code', 'name', 'location']

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'location']