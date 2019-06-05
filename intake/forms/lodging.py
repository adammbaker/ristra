from django import forms

from intake.models import Lodging

class LodgingForm(forms.ModelForm):

    class Meta:
        model = Lodging
        fields = ['lodging_type','description']
