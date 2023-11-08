from django import forms


class UploadFileForm(forms.Form):
    fName = forms.CharField(max_length=100)
    file = forms.FileField(upload_to='file/')
    fDateTime = forms.DateTimeField()
