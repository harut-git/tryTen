from django import forms
from django.shortcuts import render

from demo.forms import DmsSettingsForm, SelectDmsForm, IManageCabinetForm
from .models import *

import json
import pdb


def index(request):
    return render(request, 'demo/index.html')


## Dynamic forms demo

def dms(request):
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
    if IngForm.is_valid():
        print(ckb.dms_name)
        k = open('static/static/Configs/base_config.reg', 'r')
        lines = k.readlines()
        new_lines = lines
        k.close()
        new_lines.append('[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\\' + ckb.dms_name + '\n')
        path = '[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\\' + ckb.dms_name + '\n'
        for j in IngForm.cleaned_data:
            if type(IngForm.cleaned_data[j]) is int:
                base = 'dword:00000000'
                cleaned = str(hex(IngForm.cleaned_data[j])).replace('0x', '')
                base = base[:-len(cleaned)]
                IngForm.cleaned_data[j] = base + cleaned
                new_lines.insert(lines.index(path) + 1,
                                 '"{}"={}\n'.format(IngForm.fields[j].label, IngForm.cleaned_data[j]))
            else:
                new_lines.insert(lines.index(path) + 1,
                                 '"{}"="{}"\n'.format(IngForm.fields[j].label, IngForm.cleaned_data[j]))
        k = open('static/static/Configs/generated.reg', 'w+')
        k.writelines(new_lines)
        k.close()
    return render(request, "demo/dynamic.html", context)


def cabinets(request):
    context = {}
    form = IManageCabinetForm(request.POST or None)
    context['CabinetForm'] = form
    # if form.is_valid():

    return render(request, "demo/cabinet.html", context)
