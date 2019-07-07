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
    )

    class Meta:
        model = TravelPlan
        fields = ['arranged_by','confirmation','destination_city','destination_state','travel_date','city_van_date','travel_food_prepared','eta','travel_mode','notes',]
