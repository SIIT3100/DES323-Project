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

from database import views as database_views

urlpatterns = [
    path("", core_views.index),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("application/login", core_views.login, name="core_views_login"),
    path("application/logins/fn.hidden", database_views.database_login,name="database_login"),
    path("application/register", core_views.signup, name="register"),
    path("application/register/fn.hidden", database_views.database_create_new_user,name="database_create_new_user"),
    path("application/home/<uid>", database_views.database_item_upload, name="database_item_upload"), # home/upload
    path("application/home.result", core_views.home2), # result
    path("application/home.result/<fid>", database_views.database_statistic, name="database_homeShowTest"),
    path("application/files/add/<uid>", database_views.database_item_add,name="database_item_add"),
    path("application/files/<fuid>", database_views.database_item_list_by_id),
    #path("application/files/s/<fuid>", # specific file)
    path("application/files/delete/<fid>", database_views.database_item_delete),
    path("application/files/edit/<fid>", database_views.database_item_edit, name="database_item_edit"),
    #path("application/files/update", database_views.database_update, name="database_update"),
    path("api/delete/<id>", database_views.api_item_delete),
    path("api/process/<id>", database_views.api_item_process),
    #path('submit_messages/', database_views.submit_messages, name='submit_messages'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)