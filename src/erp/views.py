from django.shortcuts import render

def dashboard(request):
    ctx = {}
    return render(request, 'dashboard.html', ctx)