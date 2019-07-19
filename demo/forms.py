from django import forms
from .models import DMS


# class HamburgerForm(forms.ModelForm):
#    class Meta:
#        model = Ingridients
#        fields = ['cheese', 'ham', 'onion', 'bread', 'ketchup']

# class PancakeForm(forms.ModelForm):
#    class Meta:
#        model = Ingridients
#        fields = ['milk', 'butter', 'honey', 'eggs']


class SelectDmsForm(forms.ModelForm):
    class Meta:
        model = DMS
        exclude = ['dms_settings']


class DmsSettingsForm(forms.Form):
    pass


class IManageCabinetForm(forms.Form):
    cabinet_id = forms.CharField(required=True, label='CabinetId')
    prediction_attributes = forms.CharField(required=True, label='PredictionAttributes')
    default_folder_for_email = forms.CharField(required=True, label='DefaultFolderForEmail')
    default_class_for_email = forms.CharField(required=False, label='DefaultClassForEmail')
    side_pane_attributes = forms.CharField(required=True, label='SidePaneAttributes')
    top_pane_attributes = forms.CharField(required=True, label='TopPaneAttributes')
