from django import forms
from django.shortcuts import render, redirect

from demo.forms import DmsSettingsForm, SelectDmsForm, IManageCabinetForm, OutlookAddinForm
from .models import *

import json

CURRENT_DMS = ''


def add_to_config_by_path(form, path, lines):
    new_lines = lines
    if path in lines:
        print("-----------------------------------", path)
        for j in form.fields:
            if type(form.cleaned_data[j]) is int:
                base = 'dword:00000000'
                cleaned = str(hex(form.cleaned_data[j])).replace('0x', '')
                base = base[:-len(cleaned)]
                form.cleaned_data[j] = base + cleaned
                new_lines.insert(lines.index(path) + 1, '"{}"={}\n'.format(form.fields[j].label, form.cleaned_data[j]))
            else:
                new_lines.insert(lines.index(path) + 1,
                                 '"{}"="{}"\n'.format(form.fields[j].label, form.cleaned_data[j]))
    return new_lines


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
    dms_form = SelectDmsForm(request.POST or None)
    context['dms_form'] = dms_form
    if IngForm.is_valid():
        global CURRENT_DMS
        CURRENT_DMS = ckb.dms_name
        k = open('static/static/Configs/base_config.reg', 'r')
        lines = k.readlines()
        new_lines = lines
        k.close()
        new_lines.insert(lines.index("[HKEY_CURRENT_USER\Software\Zero\OutlookAddin]\n") + 1,
                         '"{}"="{}"\n'.format('CurrentDms', CURRENT_DMS))
        new_lines.append('[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\\' + ckb.dms_name + ']' + '\n')
        new_lines.append(
            '[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\\' + ckb.dms_name + '\\' 'Cabinets' + ']' + '\n')
        path = '[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\\' + ckb.dms_name + ']' + '\n'
        for j in IngForm.cleaned_data:
            if type(IngForm.cleaned_data[j]) is int or IngForm.cleaned_data[j].isdigit():
                base = 'dword:00000000'
                cleaned = str(hex(int(IngForm.cleaned_data[j]))).replace('0x', '')
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
        return redirect('cabinets')
    return render(request, "demo/dynamic.html", context)


def cabinets(request):
    context = {}
    form = IManageCabinetForm(request.POST or None)
    context['CabinetForm'] = form
    if form.is_valid():
        path = '[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\\' + CURRENT_DMS + '\\' + 'Cabinets\\' + \
               form.cleaned_data[
                   'cabinet_id'] + ']' + '\n'
        k = open('static/static/Configs/generated.reg', 'r+')
        new_lines = k.readlines()
        k.close()
        if path in new_lines:
            context['cabinet_exists'] = 1
            return render(request, "demo/cabinet.html", context)
        new_lines.append(path)
        print(new_lines)
        for j in form.cleaned_data:
            if j == 'cabinet_id':
                continue
            if type(form.cleaned_data[j]) is int:
                base = 'dword:00000000'
                cleaned = str(hex(form.cleaned_data[j])).replace('0x', '')
                base = base[:-len(cleaned)]
                form.cleaned_data[j] = base + cleaned
                new_lines.insert(new_lines.index(path) + 1,
                                 '"{}"={}\n'.format(form.fields[j].label, form.cleaned_data[j]))
            else:
                new_lines.insert(new_lines.index(path) + 1,
                                 '"{}"="{}"\n'.format(form.fields[j].label, form.cleaned_data[j]))
        f = open('static/static/Configs/generated.reg', 'w+')
        f.writelines(new_lines)
        f.close()
    return render(request, "demo/cabinet.html", context)


def finalize(request):
    context = {}
    form = OutlookAddinForm(request.POST or None)
    confirm_message = None
    if form.is_valid():
        k = open('static/static/Configs/generated.reg', 'r+')
        new_lines = k.readlines()
        k.close()
        lines = add_to_config_by_path(form, path="[HKEY_CURRENT_USER\Software\Zero\OutlookAddin]\n", lines=new_lines)
        f = open('static/static/Configs/generated.reg', 'w+')
        f.writelines(lines)
        f.close()
        confirm_message = 'Your configuration file is ready!'
        form = None
    context['OutlookAddinForm'] = form
    context['confirm_message'] = confirm_message
    return render(request, "demo/finalize.html", context)
