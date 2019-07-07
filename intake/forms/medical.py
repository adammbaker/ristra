from django import forms
from intake.models import Medical

# Create your forms here.
class MedicalForm(forms.ModelForm):
    resolved = forms.BooleanField(required=False)
    
    class Meta:
        model = Medical
        fields = ['provider','description','resolved','notes',]
