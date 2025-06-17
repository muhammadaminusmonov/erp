# from django.urls import path
# from .views import (
#     order_list,
#     order_detail,
#     order_create,
#     order_update,
#     order_delete,
#     update_order_status
# )
#
# urlpatterns = [
#     path('', order_list, name='order_list'),
#     path('create/', order_create, name='order_create'),
#     path('<int:pk>/', order_detail, name='order_detail'),
#     path('<int:pk>/edit/', order_update, name='order_update'),
#     path('<int:pk>/delete/', order_delete, name='order_delete'),
#     path('<int:pk>/status/<str:status>/', update_order_status, name='update_order_status'),
# ]

# order/urls.py
from django.urls import path
from .views import OrderPrintView

from . import views
from .views import OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView, OrderDeleteView

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/<int:pk>/update-status/<str:status>/', views.update_order_status, name='update_order_status'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('order/<int:pk>/print/', OrderPrintView.as_view(), name='order_print'),

]