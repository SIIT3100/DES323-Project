from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def list(request):
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

            new_user = User(username=username, email=email, password=password)
            new_user.save()

            messages.success(request, 'You are registered and can now log in')
            return redirect('application/login')  # Redirect to the login page
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('application/register')  # Redirect to the signup page

    return render(request, 'WebApp/list_view.html')


