from django import forms
from intake.models import IntakeBus

# Create your forms here.
class IntakeBusForm(forms.ModelForm):
    class Meta:
        model = IntakeBus
        fields = ['origin','state','arrival_time','number','notes',]
