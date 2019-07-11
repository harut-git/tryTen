from django.shortcuts import render


# Create your views here.


def products(request):
    context = {}
    template = 'products.html'
    return render(request, template, context)
