from fileinput import FileInput
from pyexpat import model
from tkinter import Button
from unicodedata import name
from django.forms import CharField, FileField, forms

class UploadFileClass(forms.Form):
    #title = CharField(max_length=50) #html
    file = FileField(label="files")