from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms

from intake.models import IntakeBuses

class IntakeBusForm(forms.ModelForm):
    arrival_time = forms.DateTimeField(
        required=True,
        widget=DateTimePickerInput(format='%m/%d/%Y %H:%M')
    )

    class Meta:
        model = IntakeBuses
        fields = ['arrival_time','number','origin','destination','notes']
