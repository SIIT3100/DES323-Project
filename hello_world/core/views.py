from django.shortcuts import render

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

def login(request):
    context = {}
    return render(request, "WebApp/login.html", context=context)

def signup(request):
   context = {}
   return render(request, 'WebApp/reg.html', context=context)

def home(request):
   context = {}
   return render(request, "WebApp/home.html", context=context)

