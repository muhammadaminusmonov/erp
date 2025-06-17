from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Inventory
from django.db.models import Sum, Count
from category.models import Category

def inventory_view(request):
    # Inventar ro'yxatini olish
    inventory_items = Inventory.objects.all().select_related('product', 'category')

    # Qidiruv funksiyasi
    query = request.GET.get('q')
    if query:
        inventory_items = inventory_items.filter(title__icontains=query)

    # Sahifalash
    paginator = Paginator(inventory_items, 5)  # Har sahifada 5 ta element
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Umumiy statistika
    total_items = inventory_items.count()
    low_stock = inventory_items.filter(stock__lte=5).count()
    total_value = inventory_items.aggregate(total=Sum('price'))['total'] or 0
    total_categories = Category.objects.count()

    context = {
        'inventory_items': page_obj,
        'page_obj': page_obj,
        'total_items': total_items,
        'low_stock': low_stock,
        'total_value': total_value,
        'total_categories': total_categories,
    }
    return render(request, 'inventory.html', context)

def add_inventory(request):
    # Inventar qo'shish logikasi (form bilan ishlash)
    pass

def view_inventory(request, id):
    # Inventar detallarini ko'rsatish
    pass

def restock_inventory(request, id):
    # Inventarni to'ldirish logikasi
    pass

def edit_inventory(request, id):
    # Inventarni tahrirlash logikasi
    pass


from .forms import InventoryForm
from django.contrib import messages


def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item added successfully!')
            return redirect('inventory')
        else:
            messages.error(request, form)
    else:
        form = InventoryForm()

    context = {
        'form': form,
    }
    return render(request, 'add_inventory.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventory
from django.contrib import messages

def view_inventory(request, id):
    inventory_item = get_object_or_404(Inventory, id=id)
    context = {
        'item': inventory_item,
    }
    return render(request, 'view_inventory.html', context)

def restock_inventory(request, id):
    inventory_item = get_object_or_404(Inventory, id=id)
    if request.method == 'POST':
        new_stock = request.POST.get('stock')
        if new_stock:
            inventory_item.stock += int(new_stock)
            inventory_item.save()
            messages.success(request, 'Inventory restocked successfully!')
            return redirect('inventory')
    context = {
        'item': inventory_item,
    }
    return render(request, 'restock_inventory.html', context)

def edit_inventory(request, id):
    inventory_item = get_object_or_404(Inventory, id=id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item updated successfully!')
            return redirect('inventory')
    else:
        form = InventoryForm(instance=inventory_item)
    context = {
        'form': form,
        'item': inventory_item,
    }
    return render(request, 'edit_inventory.html', context)