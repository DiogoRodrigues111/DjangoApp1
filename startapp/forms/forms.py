from django.forms import CharField, FileField, forms

class UploadFileClass(forms.Form):
    title = CharField(max_length=50)
    file = FileField()