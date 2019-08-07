from django import forms
from intake.models import Campaign

from bootstrap_datepicker_plus import DateTimePickerInput

# Create your forms here.
class CampaignForm(forms.ModelForm):
    expiration_date = forms.DateTimeField(
        help_text='Time at which this link will expire',
        widget=DateTimePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"}
        ),
    )

    class Meta:
        model = Campaign
        fields = ['organization','expiration_date',]
