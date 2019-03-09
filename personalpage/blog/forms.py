from django import forms
from django.conf import settings

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.ImageField()

class FileHandler():
    def write_file(self, f):
        static_root = settings.STATIC_ROOT
        file_path   = static_root + '/blog/uploads/' + f.name
        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
