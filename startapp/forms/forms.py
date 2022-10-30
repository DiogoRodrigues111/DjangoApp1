from django.forms import BooleanField, forms, fields, widgets, models


class UploadFileClass(forms.Form):
    file = forms.FileField(required=False)


class PgSignInRegister(forms.Form):
    name = fields.CharField(required=True)
    email = fields.EmailField(required=True)
    password = fields.CharField(required=True, widget=widgets.PasswordInput(), label='Enter with password')
    bool_banned = fields.BooleanField(initial=False, required=False, show_hidden_initial=True)


class PgUpdate(forms.Form):
    name = fields.CharField(required=True)
    email = fields.EmailField(required=True)
    password = fields.CharField(widget=widgets.PasswordInput(), label='Enter with password')


class PgDelete(forms.Form):
    email = fields.EmailField(required=True)


class PgBanned(forms.Form):
    bool_banned = fields.BooleanField(initial=False, required=True)
    email = fields.EmailField(required=True)


class PgUnbanned(forms.Form):
    bool_banned = fields.BooleanField(initial=True, required=False)
    email = fields.EmailField(required=True)


class Login(forms.Form):
    email = fields.EmailField(required=True)
    password = fields.CharField(widget=widgets.PasswordInput(), label='Enter with password')


class CheckLogin(forms.Form):
    email = fields.EmailField()


class SendEmail(forms.Form):
    subject = fields.CharField(required=True)
    text = fields.CharField(widget=widgets.Textarea(), required=True)
    _to = fields.EmailField(required=True)
    _from = fields.EmailField(required=True)