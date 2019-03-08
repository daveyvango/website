from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.ImageField()

class FileHandler():
    def write_file(self, f):
        with open('/tmp/uploads/uploadedfile.jpg', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
