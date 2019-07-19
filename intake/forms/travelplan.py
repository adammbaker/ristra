from django import forms
from intake.models import TravelPlan

from bootstrap_datepicker_plus import DateTimePickerInput

# Create your forms here.
class TravelPlanForm(forms.ModelForm):
    travel_date = forms.DateTimeField(
        help_text="Format YYYY-MM-DD HH:MM",
        widget=DateTimePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"}
        ),
    )
    city_van_date = forms.DateTimeField(
        help_text="Format YYYY-MM-DD HH:MM",
        widget=DateTimePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"}
        ),
    )
    eta = forms.DateTimeField(
        help_text="Format YYYY-MM-DD HH:MM",
        label='Estimated Time of Arrival',
        widget=DateTimePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"}
        ),
    )

    class Meta:
        model = TravelPlan
        fields = ['arranged_by','travel_mode','confirmation','destination_city','destination_state','travel_date','eta','city_van_date','travel_food_prepared','notes',]
