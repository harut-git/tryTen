from django import forms


class SendForm(forms.Form):
    email = forms.EmailField(required=True)
    emails_per_contact = forms.IntegerField(required=True)
