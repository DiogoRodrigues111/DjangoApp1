from django.forms import forms


class UploadFileClass(forms.Form):
    file = forms.FileField(required=False)


class PgSignInRegister(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.PasswordInput(required=True)


class PgUpdate(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.PasswordInput(required=True)


class PgDelete(forms.Form):
    email = forms.EmailField(required=True)