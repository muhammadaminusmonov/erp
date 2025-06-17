from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta, datetime
from customer.models import Customer
from order.models import Order, OrderItem
from product.models import Product
from inventory.models import Inventory

def dashboard(request):
    # Calculate time ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)

    # Sales metrics - total o'rniga total_amount ishlating
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    today_revenue = Order.objects.filter(created_at__date=today).aggregate(total=Sum('total_amount'))['total'] or 0
    week_revenue = Order.objects.filter(created_at__date__gte=week_ago).aggregate(total=Sum('total_amount'))['total'] or 0
    month_revenue = Order.objects.filter(created_at__date__gte=month_ago).aggregate(total=Sum('total_amount'))['total'] or 0

    # Order metrics - date o'rniga created_at ishlating
    total_orders = Order.objects.count()
    today_orders = Order.objects.filter(created_at__date=today).count()
    week_orders = Order.objects.filter(created_at__date__gte=week_ago).count()
    month_orders = Order.objects.filter(created_at__date__gte=month_ago).count()

    # Customer metrics
    total_customers = Customer.objects.count()
    # last_update maydoni borligiga ishonch hosil qiling, yo'q bo'lsa created_at ishlating
    new_customers = Customer.objects.filter(join_date__date__gte=month_ago).count()

    # Inventory alerts
    low_stock_items = Inventory.objects.filter(stock__lt=10, status=1).count()

    # Recent orders (last 5) - date o'rniga created_at ishlating
    recent_orders = Order.objects.select_related('customer').prefetch_related('order_items').order_by('-created_at')[:5]

    # Inventory alerts (items with low stock)
    inventory_alerts = Inventory.objects.filter(stock__lt=10, status=1).select_related('product')[:5]

    # Customer segments - segment maydoni borligiga ishonch hosil qiling
    customer_segments = {
        'new': Customer.objects.filter(segment='1').count(),
        'regular': Customer.objects.filter(segment='2').count(),
        'vip': Customer.objects.filter(segment='3').count(),
        'inactive': Customer.objects.filter(segment='4').count(),
    }

    # Sales performance data for charts
    # Weekly sales data (last 7 days) - date o'rniga created_at ishlating
    weekly_sales = Order.objects.filter(
        created_at__date__gte=week_ago
    ).values('created_at__date').annotate(
        total=Sum('total_amount')  # total o'rniga total_amount
    ).order_by('created_at__date')

    # Monthly sales data (last 30 days grouped by week) - date o'rniga created_at
    month_start = today - timedelta(days=30)
    monthly_sales_raw = Order.objects.filter(
        created_at__date__gte=month_start
    ).values_list('created_at', 'total_amount')  # total o'rniga total_amount

    # Group by week in Python
    monthly_sales_by_week = {}
    for date, total in monthly_sales_raw:
        week_number = date.isocalendar()[1]  # ISO week number
        if week_number not in monthly_sales_by_week:
            monthly_sales_by_week[week_number] = 0
        monthly_sales_by_week[week_number] += float(total or 0)

    # Prepare weekly chart data (last 7 days)
    weekly_labels = [(today - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]
    weekly_data = [0] * 7

    for sale in weekly_sales:
        sale_date = sale['created_at__date']  # date o'rniga created_at
        day_index = (today - sale_date).days
        if 0 <= day_index <= 6:
            weekly_data[6 - day_index] = float(sale['total'] or 0)

    # Prepare monthly chart data (last 30 days grouped by week)
    monthly_labels = []
    monthly_data = [0] * 4  # 4 weeks in a month

    current_week = (today - timedelta(days=30)).isocalendar()[1]
    for i in range(4):
        week_num = current_week + i  # Get following weeks
        week_label = f"Week {i + 1}"
        monthly_labels.append(week_label)
        monthly_data[i] = float(monthly_sales_by_week.get(week_num, 0))

    # Prepare yearly chart data (last 12 months) - date o'rniga created_at
    yearly_sales_raw = Order.objects.filter(
        created_at__date__gte=year_ago
    ).values_list('created_at', 'total_amount')  # total o'rniga total_amount

    yearly_sales = {month: 0 for month in range(1, 13)}
    for date, total in yearly_sales_raw:
        month = date.month
        yearly_sales[month] += float(total or 0)

    yearly_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    yearly_data = [yearly_sales.get(month, 0) for month in range(1, 13)]

    context = {
        # Stats cards data
        'stats': [
            {
                'title': "Today's Revenue",
                'value': f"${today_revenue:,.2f}",
                'trend': 'up',
                'change': "12% from yesterday" if today_revenue > 0 else "No sales today",
            },
            {
                'title': "New Orders",
                'value': today_orders,
                'trend': 'up' if today_orders > 0 else 'down',
                'change': "8% from yesterday" if today_orders > 0 else "No orders today",
            },
            {
                'title': "Inventory Alerts",
                'value': low_stock_items,
                'trend': 'down' if low_stock_items > 0 else 'up',
                'change': "Need restocking" if low_stock_items > 0 else "All stock levels good",
            },
            {
                'title': "New Customers",
                'value': new_customers,
                'trend': 'up' if new_customers > 0 else 'down',
                'change': "2% from last week" if new_customers > 0 else "No new customers",
            },
        ],

        # Sales performance chart data
        'sales_chart': {
            'weekly': {
                'labels': weekly_labels,
                'data': weekly_data,
            },
            'monthly': {
                'labels': monthly_labels,
                'data': monthly_data,
            },
            'yearly': {
                'labels': yearly_labels,
                'data': yearly_data,
            },
        },

        # Recent orders data
        'recent_orders': [
            {
                'id': order.id,
                'customer': {
                    'first_name': order.customer.first_name,
                    'last_name': order.customer.last_name,
                    'email': order.customer.email,
                },
                'products': order.order_items.all()[:3],
                'total': order.total_amount,  # total o'rniga total_amount
                'date': order.created_at.strftime('%b %d, %Y'),  # date o'rniga created_at
                'status': order.get_status_display(),
                'status_class': order.get_status_class(),
            }
            for order in recent_orders
        ],

        # Inventory alerts data
        'inventory_alerts': [
            {
                'product': {
                    'title': item.product.title,
                    'category': item.product.category.name,
                },
                'stock': item.stock,
                'status': item.get_status_display(),
                'status_class': {
                    1: 'active',
                    2: 'out_of_stock',
                    3: 'draft',
                }.get(item.status, 'active'),
            }
            for item in inventory_alerts
        ],

        # Customer segments data
        'customer_segments': customer_segments,

        # Summary data
        'summary': {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'new_customers': new_customers,
        },
    }

    return render(request, 'dashboard.html', context)