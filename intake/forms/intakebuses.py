from django import forms

from intake.models import IntakeBuses

class IntakeBusForm(forms.ModelForm):
    class Meta:
        model = IntakeBuses
        fields = ['arrival_time','number','origin','notes']
