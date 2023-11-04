from django.db import models

# Create your models here.
class User(models.Model):
    UID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    pfp = models.URLField(max_length=500)
    
class File(models.Model):
    fID = models.AutoField(primary_key=True)
    fName = models.CharField(max_length=100)
    file = models.FileField(upload_to='file/')
    fDateTime = models.DateTimeField()
    fUID = models.ForeignKey(User, on_delete=models.CASCADE)