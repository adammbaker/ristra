from django import forms
from intake.models import Asylee

# Create your forms here.
class AsyleeForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False
    )
    class Meta:
        model = Asylee
        fields = ['name','sex','date_of_birth','phone_number','tsa_done','legal_done','notes',]
