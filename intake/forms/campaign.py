from django import forms
from intake.models import Campaign

# Create your forms here.
class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['campaign', 'organization',]
