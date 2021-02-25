from django import forms
from intake.forms.forms import DateTimeInput
from intake.models import IntakeBus

# Create your forms here.
class IntakeBusForm(forms.ModelForm):
    arrival_time = forms.DateTimeField(
        widget=DateTimeInput(),
    )

    class Meta:
        model = IntakeBus
        fields = ['origin','state','arrival_time','number','notes',]
