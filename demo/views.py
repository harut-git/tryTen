from django import forms
from django.shortcuts import render

from demo.forms import DmsSettingsForm, SelectDmsForm
from .models import *

import json
import pdb


def index(request):
    return render(request, 'demo/index.html')


## Dynamic forms demo

def dynamic(request):
    context = {}
    content = {}

    ckb = DMS.objects.last()
    if ckb == None:
        ckb = DMS.objects.create()

    if request.method == 'POST':
        if 'dms_name' in request.POST:
            ckb.dms_name = str(request.POST['dms_name'])
            ckb.save()
            try:
                content = json.loads(ckb.dms_settings)
            except json.JSONDecodeError:
                content = {}
        else:
            for key in request.POST.keys():
                if key != 'csrfmiddlewaretoken':
                    content[key] = request.POST[key]
            ckb.ingridients = json.dumps(content)
            ckb.save()

    if ckb.dms_name == 'iManage':
        new_fields = {
            'BaseUri': forms.URLField(required=True, label='BaseUri'),
            'SupportedAuthType': forms.ChoiceField(required=True, label='SupportedAuthType',
                                                   choices=((0, 'OAuth2'),
                                                            (1, 'SAML2'),
                                                            (2, 'Session'),
                                                            (3, 'Kerberos '))),
            'AppId': forms.CharField(required=True, label='AppId')}
    else:
        new_fields = {
            'RepositoryId': forms.CharField(required=True, label='RepositoryId'),
            'ApiUri': forms.URLField(required=True, label='ApiUri'),
            'SupportedAuthType': forms.ChoiceField(required=True, label='SupportedAuthType',
                                                   choices=((0, 'OAuth2'),
                                                            (1, 'SAML2'),
                                                            (2, 'Session'),
                                                            (3, 'Kerberos '))),
            'AppId': forms.CharField(required=True, label='AppId')}

    DynamicIngridientsForm = type('DynamicIngridientsForm',
                                  (DmsSettingsForm,),
                                  new_fields)

    IngForm = DynamicIngridientsForm(content)
    context['dms_settings_form'] = IngForm
    context['dms_form'] = SelectDmsForm(request.POST or None)
    return render(request, "demo/dynamic.html", context)
