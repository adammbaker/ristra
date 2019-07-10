from django import forms
from intake.models import TravelPlan

# Create your forms here.
class TravelPlanForm(forms.ModelForm):
    travel_date = forms.DateTimeField(
        help_text="Format YYYY-MM-DD HH:MM",
    )
    city_van_date = forms.DateTimeField(
        help_text="Format YYYY-MM-DD HH:MM",
    )
    eta = forms.DateTimeField(
        help_text="Format YYYY-MM-DD HH:MM",
        label='Estimated Time of Arrival'
    )

    class Meta:
        model = TravelPlan
        fields = ['arranged_by','travel_mode','confirmation','destination_city','destination_state','travel_date','eta','city_van_date','travel_food_prepared','notes',]
