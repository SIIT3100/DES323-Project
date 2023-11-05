from django.contrib import admin

from database.models import *

# Register your models here.
@admin.register(User)
class User_admin(admin.ModelAdmin):
    pass

@admin.register(File)
class File_admin(admin.ModelAdmin):
    pass