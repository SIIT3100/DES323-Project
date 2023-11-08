from django.shortcuts import render
from django.http import HttpResponse
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
    context = {}
    return render(request, 'WebApp/reg.html', context=context)

def home1(request):
   context = {}
   return render(request, "WebApp/home.html", context=context)

def home2test(request):
    context = {}
    return render(request, "WebApp/homeShow.html", context=context)

def home2(request):
    context = {}
    return render(request, "WebApp/homeShowTest.html", context=context)

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
