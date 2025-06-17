from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_view, name='customer'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/<int:id>/', views.view_customer, name='view_customer'),
    path('customers/<int:id>/message/', views.message_customer, name='message_customer'),
    path('customers/<int:id>/edit/', views.edit_customer, name='edit_customer'),
    # Boshqa marshrutlar
]