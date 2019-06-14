from django import forms

from intake.models import Location

class LocationForm(forms.ModelForm):
    name = forms.CharField(help_text='Name of the location', required=True)

    class Meta:
        model = Location
        fields = ['organization','name','notes']
