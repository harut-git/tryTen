from django import forms


class SendForm(forms.Form):
    email = forms.EmailField(required=True, label="Email:")
    emails_per_contact = forms.IntegerField(required=True, label="Emails per Contact:")
    exchange_username = forms.EmailField(required=False, label="Exchange Email:")
    exchange_pswd = forms.CharField(required=False, widget=forms.PasswordInput, label="Exchange Password:")
    conversations_per_contact = forms.IntegerField(required=False, label="Conversations per Contact:")
    thread_count_in_coversation = forms.IntegerField(required=False, label="Threads count per Conversation:")
