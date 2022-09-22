from django.forms import forms


class UploadFileClass(forms.Form):
    file = forms.FileField(required=False)
