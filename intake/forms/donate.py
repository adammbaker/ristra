from django import forms
from intake.models import Donate, Organization

# Create your forms here.
class DonateForm(forms.ModelForm):
    class Meta:
        model = Donate
        fields = ['name', 'location','url','description',]
