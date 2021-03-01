from django import forms
from intake.forms.forms import DateTimeInput
from intake.models import Campaign

# Create your forms here.
class CampaignForm(forms.ModelForm):
    expiration_date = forms.DateTimeField(
        help_text='Time at which this link will expire',
        widget=DateTimeInput(),
    )

    class Meta:
        model = Campaign
        fields = ['organization','expiration_date',]
