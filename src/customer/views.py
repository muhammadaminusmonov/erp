from django.shortcuts import render

def customer(request):
    ctx = {}
    return render(request, 'customer.html', ctx)