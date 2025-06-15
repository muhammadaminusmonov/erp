from django.shortcuts import render

def order(request):
    ctx = {}
    return render(request, 'order.html', ctx)