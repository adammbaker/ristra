from django import forms
from intake.models import IntakeBus

from bootstrap_datepicker_plus import DateTimePickerInput

# Create your forms here.
class IntakeBusForm(forms.ModelForm):
    arrival_time = forms.DateTimeField(
        widget=DateTimePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"}
        ),
    )

    class Meta:
        model = IntakeBus
        fields = ['origin','state','arrival_time','number','notes',]
