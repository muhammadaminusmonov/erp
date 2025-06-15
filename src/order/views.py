from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q
from django.utils import timezone
from .models import Order, Customer
from .forms import OrderForm


def order_list(request):
    # Get filter parameters from request
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')

    # Base queryset
    orders = Order.objects.select_related('customer').all().order_by('-created_at')

    # Apply filters
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    if search_query:
        orders = orders.filter(
            Q(id__icontains=search_query) |
            Q(customer__name__icontains=search_query) |
            Q(customer__email__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Today's summary data
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today)

    summary_data = {
        'new_orders': today_orders.count(),
        'total_revenue': today_orders.aggregate(total=Sum('total_amount'))['total'] or 0,
        'to_ship': today_orders.filter(status='processing').count(),
        'returns': today_orders.filter(status='returned').count(),
    }

    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'summary_data': summary_data,
        'page_title': 'Order Management',
    }

    return render(request, 'order.html', context)


def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('customer'), pk=pk)

    context = {
        'order': order,
        'page_title': f'Order #{order.id}',
    }

    return render(request, 'order_detail.html', context)


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()

    context = {
        'form': form,
        'page_title': 'Create New Order',
    }

    return render(request, 'order_form.html', context)


def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)

    context = {
        'form': form,
        'order': order,
        'page_title': f'Edit Order #{order.id}',
    }

    return render(request, 'order_form.html', context)


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('order_list')

    context = {
        'order': order,
        'page_title': f'Delete Order #{order.id}',
    }

    return render(request, 'order_confirm_delete.html', context)


def update_order_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk)

    if status in dict(Order.STATUS_CHOICES).keys():
        order.status = status
        order.save()

    return redirect('order_detail', pk=order.pk)