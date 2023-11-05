from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import User
import os

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

def login(request):
    context = {}
    return render(request, "WebApp/login.html", context=context)

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('application/register')  # Redirect to the signup page if username exists

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered')
                return redirect('application/register')  # Redirect to the signup page if email exists

            # Create a new user with Django's built-in create_user method
            new_user = User(username=username, email=email, password=password)
            new_user.save()

            messages.success(request, 'You are registered and can now log in')
            return redirect('application/login')  # Redirect to the login page
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('application/register')  # Redirect to the signup page

    return render(request, 'WebApp/reg.html')

def home(request):
   context = {}
   return render(request, "WebApp/home.html", context=context)

def testContent(request):
    context = {}
    return render(request, "WebApp/testPage.html", context=context)

def uploadfile(request):
    context = {}
    return render(request, "WebApp/upload.html", context=context)

def view_file(request):
    file_path = "/path/to/your/uploaded/file"  # Set the actual file path
    file_name = os.path.basename(file_path)
    file_type = "application/octet-stream"  # Set the appropriate MIME type

    context = {
        'file_path': file_path,
        'file_name': file_name,
        'file_type': file_type,
    }

    return render(request, "WebApp/view.html", context=context)

def download_file(request):
    file_path = "/path/to/your/uploaded/file"  # Set the actual file path
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
    
def edit_file(request):
    context = {}
    return render(request, "WebApp/editfile.html", context=context)

def save_edited_file(request):
    if request.method == 'POST':
        edited_file = request.FILES.get('edited_file')

    return HttpResponse("File saved successfully")
