from django import forms
from intake.forms.forms import DateInput, DateTimeInput, TimeInput
from intake.models import TravelPlan

from datetime import datetime, timedelta

tomorrow_dt = (datetime.now() + timedelta(1)).strftime('%Y-%m-%dT%H:%M')

# Create your forms here.
class TravelPlanForm(forms.ModelForm):
    travel_date = forms.DateTimeField(
        help_text="Format MM/DD/YYYY HH:MM",
        widget=DateTimeInput(
            attrs={
                'min':'2020-01-01T00:00:00',
                'max':'2100-12-31T00:00:00',
                'pattern':'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}',
            }
        ),
        initial=tomorrow_dt,
    )
    city_van_date = forms.DateTimeField(
        help_text="Format MM/DD/YYYY HH:MM",
        widget=DateTimeInput(
            attrs={
                'min':'2020-01-01T00:00:00',
                'max':'2100-12-31T00:00:00',
                'pattern':'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}',
            }
        ),
        initial=tomorrow_dt,
    )
    eta = forms.DateTimeField(
        help_text="Format MM/DD/YYYY HH:MM",
        label='Estimated Time of Arrival',
        widget=DateTimeInput(
            attrs={
                'min':'2020-01-01T00:00:00',
                'max':'2100-12-31T00:00:00',
                'pattern':'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}',
            }
        ),
        initial=tomorrow_dt,
    )

    class Meta:
        model = TravelPlan
        fields = [
            'travel_mode',
            'confirmation',
            'destination_city',
            'destination_state',
            'travel_date',
            'eta',
            'city_van_date',
            'notes',
        ]


class AirlineTravelPlanForm(forms.ModelForm):
    layovers = forms.CharField(
        help_text='First leg destination',
        required=True,
    )
    class Meta:
        model = TravelPlan
        fields = ['flight_number', 'layovers',]

class BusTravelPlanForm(forms.ModelForm):
    layovers = forms.CharField(
        help_text='Cities to change',
        required=True,
    )
    class Meta:
        model = TravelPlan
        fields = ['layovers',]
