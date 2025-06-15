from django.shortcuts import render

def product(request):
    ctx = {}
    return render(request, 'product.html', ctx)