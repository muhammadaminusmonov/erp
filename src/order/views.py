# from django.shortcuts import render, redirect, get_object_or_404
# from django.core.paginator import Paginator
# from django.db.models import Sum, Count, Q
# from django.utils import timezone
# from .models import Order, Customer
# from .forms import OrderForm
#
#
# def order_list(request):
#     # Get filter parameters from request
#     status_filter = request.GET.get('status', 'all')
#     search_query = request.GET.get('search', '')
#
#     # Base queryset
#     orders = Order.objects.select_related('customer').all().order_by('-created_at')
#
#     # Apply filters
#     if status_filter != 'all':
#         orders = orders.filter(status=status_filter)
#
#     if search_query:
#         orders = orders.filter(
#             Q(id__icontains=search_query) |
#             Q(customer__name__icontains=search_query) |
#             Q(customer__email__icontains=search_query)
#         )
#
#     # Pagination
#     paginator = Paginator(orders, 10)  # Show 10 orders per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     # Today's summary data
#     today = timezone.now().date()
#     today_orders = Order.objects.filter(created_at__date=today)
#
#     summary_data = {
#         'new_orders': today_orders.count(),
#         'total_revenue': today_orders.aggregate(total=Sum('total_amount'))['total'] or 0,
#         'to_ship': today_orders.filter(status='processing').count(),
#         'returns': today_orders.filter(status='returned').count(),
#     }
#
#     context = {
#         'page_obj': page_obj,
#         'status_filter': status_filter,
#         'search_query': search_query,
#         'summary_data': summary_data,
#         'page_title': 'Order Management',
#     }
#
#     return render(request, 'order_list.html', context)
#
#
# def order_detail(request, pk):
#     order = get_object_or_404(Order.objects.select_related('customer'), pk=pk)
#
#     context = {
#         'order': order,
#         'page_title': f'Order #{order.id}',
#     }
#
#     return render(request, 'order_detail.html', context)
#
#
# def order_create(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             return redirect('order_detail', pk=order.pk)
#     else:
#         form = OrderForm()
#
#     context = {
#         'form': form,
#         'page_title': 'Create New Order',
#     }
#
#     return render(request, 'order_form.html', context)
#
#
# def order_update(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#
#     if request.method == 'POST':
#         form = OrderForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             return redirect('order_detail', pk=order.pk)
#     else:
#         form = OrderForm(instance=order)
#
#     context = {
#         'form': form,
#         'order': order,
#         'page_title': f'Edit Order #{order.id}',
#     }
#
#     return render(request, 'order_form.html', context)
#
#
# def order_delete(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#
#     if request.method == 'POST':
#         order.delete()
#         return redirect('order_list')
#
#     context = {
#         'order': order,
#         'page_title': f'Delete Order #{order.id}',
#     }
#
#     return render(request, 'order_confirm_delete.html', context)
#
#
# def update_order_status(request, pk, status):
#     order = get_object_or_404(Order, pk=pk)
#
#     if status in dict(Order.STATUS_CHOICES).keys():
#         order.status = status
#         order.save()
#
#     return redirect('order_detail', pk=order.pk)
from time import timezone

from django.shortcuts import get_object_or_404, redirect
# from django.shortcuts import render, redirect, get_object_or_404
#
# from order.models import Order
#
#
# def order(request):
#     ctx = {}
#     return render(request, 'order_list.html')
from datetime import datetime
from .models import Order, OrderItem
from customer.models import Customer
from product.models import Product
import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages



class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status and status in dict(Order.STATUS_CHOICES).keys():
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', 'all')
        return context



class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'




class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order_form.html'
    fields = ['customer', 'items', 'total_amount', 'status']
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        # Add any custom logic here before saving
        return super().form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order_confirm_delete.html'
    success_url = reverse_lazy('order_list')




def update_order_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk)
    if status in dict(Order.STATUS_CHOICES).keys():
        order.status = status
        order.save()
        messages.success(request, f"Order #{order.id} status updated to {order.get_status_display()}.")
    else:
        messages.error(request, "Invalid status.")
    return redirect('order_detail', pk=order.id)


class OrderCreateView(CreateView):
    model = Order
    template_name = 'order_create.html'
    fields = ['customer', 'total_amount', 'status']  # 'items' olib tashlandi
    success_url = reverse_lazy('order_list')
    payment_status = 'unpaid',

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all()
        context['today'] = datetime.now().date()
        return context

    def post(self, request, *args, **kwargs):
        # Extract data from form
        customer_id = request.POST.get('customer')
        order_date = request.POST.get('order_date')
        status = request.POST.get('status')
        payment_status = request.POST.get('payment_status') or 1
        shipping_address = request.POST.get('shipping_address', '')
        billing_address = request.POST.get('billing_address', '')
        notes = request.POST.get('notes', '')
        subtotal = float(request.POST.get('subtotal', 0))
        total = float(request.POST.get('total', 0))

        # Parse items JSON
        items_json = request.POST.get('items', '[]')
        items = json.loads(items_json)

        try:
            # Create the order
            customer = Customer.objects.get(id=customer_id)

            order = Order.objects.create(
                customer=customer,
                created_at=order_date,
                status=status,
                payment_status=payment_status,
                shipping_address=shipping_address,
                billing_address=billing_address,
                notes=notes,
                subtotal=subtotal,
                total_amount=total
            )

            # Create order items
            for item in items:
                product = Product.objects.get(id=item['id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
                )

            return redirect('order_detail', pk=order.pk)

        except (Customer.DoesNotExist, Product.DoesNotExist) as e:
            messages.error(request, f"Error creating order: {str(e)}")
            return self.form_invalid(form)


from django.views.generic import DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Order


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order_form.html'
    fields = ['customer', 'total_amount', 'status']
    success_url = reverse_lazy('order_list')


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

    # O'chirishni POST so'rovi orqali amalga oshirish
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class OrderPrintView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        template = get_template('order_invoice.html')
        context = {'order': order}
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename=order_{order.id}_invoice.pdf'

        # PDF generatsiya
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('PDF yaratishda xatolik yuz berdi', status=500)
        return response



