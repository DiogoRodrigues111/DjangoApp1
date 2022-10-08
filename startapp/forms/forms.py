from django.forms import forms, fields, widgets, models


class UploadFileClass(forms.Form):
    file = forms.FileField(required=False)


class PgSignInRegister(forms.Form):
    name = fields.CharField(required=True)
    email = fields.EmailField(required=True)
    password = fields.CharField(widget=widgets.PasswordInput(), label='Enter with password')


class PgUpdate(forms.Form):
    name = fields.CharField(required=True)
    email = fields.EmailField(required=True)
    password = fields.CharField(widget=widgets.PasswordInput(), label='Enter with password')


class PgDelete(forms.Form):
    email = fields.EmailField(required=True)
