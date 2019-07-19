from django import forms
from intake.models import Location

# Create your forms here.
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'notes',]
