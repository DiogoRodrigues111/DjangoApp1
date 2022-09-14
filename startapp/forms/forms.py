from fileinput import FileInput
from pyexpat import model
from unicodedata import name
from django.forms import CharField, FileField, forms

class UploadFileClass(forms.Form):
    #title = CharField(max_length=50) #html
    file = forms.FileField(required=False)