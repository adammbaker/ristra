from django import forms
from intake.forms.forms import DateTimeInput
from intake.models import IntakeBus

# Create your forms here.
class IntakeBusForm(forms.ModelForm):
    arrival_time = forms.DateTimeField(
        widget=DateTimeInput(
            attrs={
                'min':'2020-01-01T00:00:00',
                'max':'2100-12-31T00:00:00',
                'pattern':'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}',
            }
        ),
    )

    class Meta:
        model = IntakeBus
        fields = ['origin','state','arrival_time','number','notes',]
