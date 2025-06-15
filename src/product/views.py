from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from product.models import Product
from category.models import Category
from inventory.models import Inventory
from .forms import ProductForm


def product(request):
    # Get search query
    search_query = request.GET.get('search', '')

    # Get filter parameters
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')

    # Get all products with related inventory
    products = Product.objects.select_related('category').prefetch_related('inventory').all()

    # Apply search filter
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Apply category filter
    if category_filter:
        products = products.filter(category__id=category_filter)

    # Apply status filter
    if status_filter:
        products = products.filter(status=status_filter)

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all categories for filter dropdown
    categories = Category.objects.all()

    # Prepare status choices
    status_choices = dict(Product.STATUS)

    context = {
        'products': page_obj,
        'categories': categories,
        'status_choices': status_choices,
        'search_query': search_query,
        'selected_category': category_filter,
        'selected_status': status_filter,
        'results_count': paginator.count,
    }

    return render(request, 'product.html', context)


def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product')  # Redirect to product list page
    else:
        form = ProductForm()

    context = {
        'form': form,
        'page_title': 'Add New Product',
    }
    return render(request, 'product_add.html', context)


def product_edit(request, pk):
    # For editing existing products
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'page_title': 'Edit Product',
        'is_edit': True  # Add this to distinguish between add/edit in template
    }
    return render(request, 'product_add.html', context)

def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('product')

