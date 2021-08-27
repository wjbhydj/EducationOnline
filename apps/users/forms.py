
from django import forms

class LoginForms(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)