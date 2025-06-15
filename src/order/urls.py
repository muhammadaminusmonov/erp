from django.urls import path
from .views import (
    order_list,
    order_detail,
    order_create,
    order_update,
    order_delete,
    update_order_status
)

urlpatterns = [
    path('', order_list, name='order_list'),
    path('create/', order_create, name='order_create'),
    path('<int:pk>/', order_detail, name='order_detail'),
    path('<int:pk>/edit/', order_update, name='order_update'),
    path('<int:pk>/delete/', order_delete, name='order_delete'),
    path('<int:pk>/status/<str:status>/', update_order_status, name='update_order_status'),
]