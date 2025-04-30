# sysadmin/views.py
from django.shortcuts import render

def index(request):
    # Explicitly specify the path to the template for sysadmin
    return render(request, 'sysadmin/admin.html')
