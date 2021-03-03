from django import forms
from intake.models import Sponsor

# Create your forms here.
class SponsorForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False
    )
    relation = forms.CharField(
        required=False
    )

    class Meta:
        model = Sponsor
        fields = ['name','phone_number','address','city','state','zip_code','relation','notes',]
