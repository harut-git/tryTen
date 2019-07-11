from django.core.mail import send_mail
from django.shortcuts import render


# Create your views here.
from contact.forms import GenerateForm
from tryTen import settings


def products(request):
    context = {}
    template = 'products.html'
    return render(request, template, context)


def generate_form(request):
    title = 'Generate'
    form = GenerateForm(request.POST or None)
    confirm_message = None

    if form.is_valid():
        f = open('filename.reg', 'w+')
        f.write("")

    context = {'title': title, 'form': form, 'confirm_message': confirm_message, }
    template = 'contact.html'
    return render(request, template, context)
