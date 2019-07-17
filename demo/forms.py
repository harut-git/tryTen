from django import forms
from .models import DMS

#class HamburgerForm(forms.ModelForm):
#    class Meta:
#        model = Ingridients
#        fields = ['cheese', 'ham', 'onion', 'bread', 'ketchup']

#class PancakeForm(forms.ModelForm):
#    class Meta:
#        model = Ingridients
#        fields = ['milk', 'butter', 'honey', 'eggs']


class SelectDmsForm(forms.ModelForm):
    class Meta:
        model = DMS
        exclude = ['dms_settings']


class DmsSettingsForm(forms.Form):
    pass
