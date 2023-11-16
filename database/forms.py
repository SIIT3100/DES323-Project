from django import forms
from .models import File

class FileUpdateForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']