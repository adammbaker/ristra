from django import forms

from intake.models import Locations

class LocationForm(forms.ModelForm):
    name = forms.CharField(help_text='Name of the location', required=True)

    class Meta:
        model = Locations
        fields = ['name','notes']
