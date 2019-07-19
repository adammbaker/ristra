from django import forms
from intake.models import Asylee

from bootstrap_datepicker_plus import DatePickerInput

# Create your forms here.
class AsyleeForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False
    )
    date_of_birth = forms.DateField(
        widget=DatePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"}
        )
    )
    class Meta:
        model = Asylee
        fields = ['name','sex','date_of_birth','phone_number','tsa_done','legal_done','notes',]
