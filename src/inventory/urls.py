from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory_view, name='inventory'),
    path('inventory/add/', views.add_inventory, name='add_inventory'),
    path('inventory/<int:id>/', views.view_inventory, name='view_inventory'),
    path('inventory/<int:id>/restock/', views.restock_inventory, name='restock_inventory'),
    path('inventory/<int:id>/edit/', views.edit_inventory, name='edit_inventory'),

]