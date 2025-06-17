from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Customer
from django.db.models import Sum
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

def customer_view(request):
    # Barcha mijozlarni olish
    customers = Customer.objects.all()

    # Qidiruv funksiyasi
    query = request.GET.get('q')
    if query:
        customers = customers.filter(
            first_name__icontains=query) | customers.filter(
            last_name__icontains=query) | customers.filter(
            email__icontains=query)

    # Segmentlarni hisoblash
    new_customers = customers.filter(segment='1').count()
    regular_customers = customers.filter(segment='2').count()
    vip_customers = customers.filter(segment='3').count()
    inactive_customers = customers.filter(segment='4').count()

    # Oy ichidagi buyurtmalar va xarajatlar
    current_month = datetime.now().month
    for customer in customers:
        orders_this_month = customer.orders if customer.last_update.month == current_month else 0
        spent_this_month = customer.total_spent if customer.last_update.month == current_month else 0
        customer.orders_this_month = orders_this_month
        customer.spent_this_month = spent_this_month

    # Sahifalash
    paginator = Paginator(customers, 5)  # Har sahifada 5 ta mijoz
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'customers': page_obj,
        'page_obj': page_obj,
        'new_customers': new_customers,
        'regular_customers': regular_customers,
        'vip_customers': vip_customers,
        'inactive_customers': inactive_customers,
    }
    return render(request, 'customer.html', context)

def add_customer(request):
    if request.method == 'POST':
        # Forma bilan ishlash logikasi qo'shiladi
        pass
    return render(request, 'add_customer.html')

def view_customer(request, id):
    customer = Customer.objects.get(id=id)
    context = {'customer': customer}
    return render(request, 'view_customer.html', context)

def message_customer(request, id):
    customer = Customer.objects.get(id=id)
    context = {'customer': customer}
    return render(request, 'message_customer.html', context)

def edit_customer(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == 'POST':
        # Tahrirlash logikasi qo'shiladi
        pass
    context = {'customer': customer}
    return render(request, 'edit_customer.html', context)


from django.shortcuts import render, redirect
from .forms import CustomerForm
from django.contrib import messages


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customer')
        else:
            messages.error(request, form)
    else:
        form = CustomerForm()

    context = {
        'form': form,
    }
    return render(request, 'add_customer.html', context)