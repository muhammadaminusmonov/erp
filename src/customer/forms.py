from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'segment', 'orders', 'total_spent']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'segment': forms.Select(attrs={'class': 'form-control'}),
            'orders': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of orders'}),
            'total_spent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter total spent'}),
        }