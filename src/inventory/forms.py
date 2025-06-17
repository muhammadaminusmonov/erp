from django import forms
from .models import Inventory
from category.models import Category
from product.models import Product

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'title', 'category', 'price', 'stock', 'status', 'code', 'size', 'color']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product title'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter SKU'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter size'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter color'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }