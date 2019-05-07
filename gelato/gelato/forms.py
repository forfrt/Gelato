
from gelato import models
from django.forms import Form, ModelForm, CharField, ChoiceField, RadioSelect

class AdminProfileForm(Form):
    position        = CharField(label='position', max_length=255)
    email           = CharField(label='email', max_length=255)
    name            = CharField(label='name', max_length=255)
    encripted_pwd   = CharField(label='passwd', max_length=255)


class AcadeProfileForm(Form):
    email           = CharField(label='email', max_length=255)
    name            = CharField(label='name', max_length=255)
    encripted_pwd   = CharField(label='passwd', max_length=255)

class PasswdResetForm(Form):
    LABELS=(('acade', 'academic'), ('admin', 'administrator'))
    label           = ChoiceField(widget=RadioSelect, choices=LABELS)
    email           = CharField(label='email', help_text='Email', max_length=255)
