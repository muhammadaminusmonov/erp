from django.shortcuts import render

def inventory(request):
    ctx = {}
    return render(request, 'inventory.html')