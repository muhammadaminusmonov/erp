# from django import forms
# from .models import Order, OrderItem
# from customer.models import Customer
# from product.models import Product
#
# class OrderItemForm(forms.ModelForm):
#     product = forms.ModelChoiceField(
#         queryset=Product.objects.all(),
#         widget=forms.Select(attrs={
#             'class': 'form-control',
#             'onchange': 'updateProductPrice(this)'
#         })
#     )
#     quantity = forms.DecimalField(
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'min': '0.01',
#             'step': '0.01',
#             'onchange': 'calculateItemTotal(this)'
#         })
#     )
#     amount = forms.DecimalField(
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'readonly': True
#         }),
#         required=False
#     )
#
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity', 'amount']
#
# class OrderForm(forms.ModelForm):
#     customer = forms.ModelChoiceField(
#         queryset=Customer.objects.all(),
#         widget=forms.Select(attrs={
#             'class': 'form-control'
#         })
#     )
#     # date = forms.DateTimeField(
#     #     widget=forms.DateTimeInput(attrs={
#     #         'class': 'form-control',
#     #         'type': 'datetime-local'
#     #     })
#     # )
#     status = forms.ChoiceField(
#         choices=Order.STATUS,
#         widget=forms.Select(attrs={
#             'class': 'form-control'
#         })
#     )
#     total = forms.DecimalField(
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'readonly': True
#         }),
#         required=False
#     )
#
#     class Meta:
#         model = Order
#         fields = ['customer', 'date', 'status', 'total']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # If editing an existing order, set initial values
#         if self.instance.pk:
#             self.fields['date'].initial = self.instance.date.strftime('%Y-%m-%dT%H:%M')
#             self.fields['status'].initial = self.instance.status
#
# class OrderItemInlineFormSet(forms.BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#         # Validate at least one order item exists
#         if any(self.errors):
#             return
#         if not any(cleaned_data.get('product') for cleaned_data in self.cleaned_data):
#             raise forms.ValidationError("At least one product is required.")
#
# # Factory function to create formset for order items
# def get_order_item_formset(extra=1, data=None, files=None, instance=None):
#     FormSet = forms.inlineformset_factory(
#         Order,
#         OrderItem,
#         form=OrderItemForm,
#         formset=OrderItemInlineFormSet,
#         extra=extra,
#         can_delete=True
#     )
#     return FormSet(data=data, files=files, instance=instance)