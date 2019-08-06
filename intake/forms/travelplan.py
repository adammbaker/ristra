from django import forms
from intake.models import TravelPlan

from bootstrap_datepicker_plus import DateTimePickerInput

# Create your forms here.
class TravelPlanForm(forms.ModelForm):
    travel_date = forms.DateTimeField(
        help_text="Format MM/DD/YYYY HH:MM",
        widget=DateTimePickerInput(
            options={"format": "MM/DD/YYYY HH:mm"}
        ),
    )
    city_van_date = forms.DateTimeField(
        help_text="Format MM/DD/YYYY HH:MM",
        widget=DateTimePickerInput(
            options={"format": "MM/DD/YYYY HH:mm"}
        ),
    )
    eta = forms.DateTimeField(
        help_text="Format MM/DD/YYYY HH:MM",
        label='Estimated Time of Arrival',
        widget=DateTimePickerInput(
            options={"format": "MM/DD/YYYY HH:mm"}
        ),
    )

    class Meta:
        model = TravelPlan
        fields = ['travel_mode','confirmation','destination_city','destination_state','travel_date','eta','city_van_date','travel_food_prepared','notes',]
