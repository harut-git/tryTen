import time

from django.shortcuts import render

# Create your views here.
from smtp_send.Utils.PrepareDataSMTP import prepare_data, jobs, prepare_conversation_data
from smtp_send.forms import SendForm


def sender_form(request):
    title = 'Send random emails'
    form = SendForm(request.POST or None)
    confirm_message = None

    if form.is_valid():

        email = form.cleaned_data['email']
        emails_per_contact = form.cleaned_data['emails_per_contact']
        if form.cleaned_data['exchange_username']:
            for i in range(emails_per_contact):
                for j in jobs:
                    prepare_data(j, email)
                    prepare_conversation_data(j, email, form.cleaned_data['exchange_username'], form.cleaned_data['exchange_pswd'], form.cleaned_data['thread_count_in_coversation'])
                time.sleep(75)
        else:
            for i in range(emails_per_contact):
                for j in jobs:
                    prepare_data(j, email)
                time.sleep(75)
        title = "Thanks!"
        confirm_message = "Messages were sent!"
        form = None

    context = {'title': title, 'form': form, 'confirm_message': confirm_message, }
    template = 'sender.html'
    return render(request, template, context)
