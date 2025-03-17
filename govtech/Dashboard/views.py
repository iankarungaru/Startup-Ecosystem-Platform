from django.shortcuts import render, HttpResponse

def dashboard(request):
    return render(request,"dashboard.html")

def index(request):
    return render(request,"index.html")


def hello(request):
    return render(request,"hello.html")