from django.urls import path
from .views import product, product_add, product_edit, product_delete

urlpatterns = [
    path('', product, name='product'),
    path('add/', product_add, name='product_add'),
    path('edit/<int:pk>/', product_edit, name='product_edit'),
    path('delete/<int:pk>/', product_delete, name='product_delete'),
]