"""hello_world URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from . import views

from hello_world.core import views as core_views

from database import views as database_views

urlpatterns = [
    path("", core_views.index),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("application/login", core_views.login),
    path("application/register", core_views.signup),
    path("application/home", core_views.home),
    #path("application/files", core_views.view_file, name='view_file'),
    path("application/files/id/<fuid>", database_views.database_item_list_by_id),
    path("application/files/delete/<id>", database_views.database_item_delete),
    path("application/files/edit/<id>", database_views.database_item_edit),
    #path('application/files/<id>', core_views.edit_file, name='edit_file'),
    path('application/test', core_views.testContent),
    path("api/delete/<id>", database_views.api_item_delete),
    path("api/process/<id>", database_views.api_item_process),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
