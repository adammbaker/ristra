from django import forms
from intake.forms.forms import DateInput, DateTimeInput, TimeInput
from intake.models import TravelPlan

from datetime import datetime, timedelta

# Create your forms here.
class TravelPlanForm(forms.ModelForm):
    travel_date = forms.DateTimeField(
        help_text="Format MM/DD/YYYY HH:MM",
        widget=DateTimeInput(),
        initial=(datetime.now() + timedelta(1)).strftime('%Y-%m-%dT%H:%M'),
    )
    city_van_date = forms.DateTimeField(
        help_text="Format MM/DD/YYYY HH:MM",
        widget=DateTimeInput(),
        initial=(datetime.now() + timedelta(1)).strftime('%Y-%m-%dT%H:%M'),
    )
    eta = forms.DateTimeField(
        help_text="Format MM/DD/YYYY HH:MM",
        label='Estimated Time of Arrival',
        widget=DateTimeInput(),
        initial=(datetime.now() + timedelta(1)).strftime('%Y-%m-%dT%H:%M'),
    )

    class Meta:
        model = TravelPlan
        fields = ['travel_mode','confirmation','destination_city','destination_state','travel_date','eta','city_van_date','travel_food_prepared','notes',]

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
