import os

from django.core.files import File
from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from contact.forms import OutlookAddinForm, IManageForm, CabinetForm
from tryTen import settings


def add_to_config_by_path(form, path, lines):
    new_lines = lines
    if path in lines:
        print("-----------------------------------", path)
        for j in form.fields:
            if type(form.cleaned_data[j]) is int:
                base = 'dword:00000000'
                cleaned = str(hex(form.cleaned_data[j])).replace('0x', '')
                base = base[:-len(cleaned)]
                form.cleaned_data[j] = base+cleaned
                new_lines.insert(lines.index(path) + 1, '"{}"={}\n'.format(form.fields[j].label, form.cleaned_data[j]))
            else:
                new_lines.insert(lines.index(path) + 1,
                                 '"{}"="{}"\n'.format(form.fields[j].label, form.cleaned_data[j]))
    return new_lines

    # f = open('filename.reg', 'w+')
    # f.write("")


def products(request):
    context = {}
    template = 'products.html'
    return render(request, template, context)


def generate_form(request):
    form1 = OutlookAddinForm(request.POST or None, initial={
        'attributes_sync_refresh_days': 1,
        'outlook_folder_sync_depth_days': 60,
        'outlook_folder_resync_interval_min': 420,
        'outlook_folder_scan_interval_ms': 100,
        'item_resync_interval_ms': 5,
        'batch_processing_interval_ms': 50,
        'reconnect_timeout_min': 1,
        'max_archive_files': 5,
        'clean_statuses_and_categories': 1,
        'selection_timeout_ms': 5,
        'status_refresh_interval_min': 0,
        'disable_addin_subject_key': 'zero-deactivate',
        'use_categories': 1,
        'current_dms': 'iManage'
    })
    form2 = IManageForm(request.POST or None, initial={
        'supported_auth_type': 2,
        'primary_cabinet_id': 'iwork',
        'base_uri': 'https://10.1.1.5/'
    })
    form3 = CabinetForm(request.POST or None, initial={
        'prediction_attributes': '1,2,0',
        'default_folder_for_email': 'EMAIL',
        'default_class_for_email': "",
        'side_pane_attributes': "1,2,0,3",
        'top_pane_attributes': "1,2,0,3"
    })
    confirm_message = None
    if form1.is_valid() and form2.is_valid() and form3.is_valid():
        k = open('static/static/Configs/base_config.reg', 'r')
        lines = k.readlines()
        print(form1.cleaned_data['internal_domains'])
        print(form2.cleaned_data['supported_auth_type'])
        print(form3.cleaned_data['prediction_attributes'])
        a = add_to_config_by_path(form1, path="[HKEY_CURRENT_USER\Software\Zero\OutlookAddin]\n", lines=lines)
        b = add_to_config_by_path(form2, path="[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\iManage]\n", lines=a)
        c = add_to_config_by_path(form3, path="[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\iManage\Cabinets\iwork]\n", lines=b)
        k = open('static/static/Configs/generated.reg', 'w+')
        k.writelines(c)
        k.close()
        confirm_message = "Your reg file is ready!"
        form1, form2, form13 = None, None, None
    context = {'form1': form1, 'form2': form2, 'form3': form3, 'confirm_message': confirm_message}
    template = 'generate_form.html'
    return render(request, template, context)
