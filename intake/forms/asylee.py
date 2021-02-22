from django import forms
from intake.choices import COVID_VACCINE_CHOICES
from intake.models import Asylee

from bootstrap_datepicker_plus import DatePickerInput

# Create your forms here.
class AsyleeForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False
    )
    date_of_birth = forms.DateField(
        help_text="MM/DD/YYYY",
        widget=DatePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"}
        )
    )
    is_currently_sick = forms.BooleanField(
        # help_text='Is sick now'
        required=False
    )
    class Meta:
        model = Asylee
        fields = ['name','a_number','sex','date_of_birth','phone_number','tsa_done','legal_done','had_covid_disease','had_covid_vaccine', 'is_currently_sick','notes',]

class AsyleeHealthFollowUpForm(forms.ModelForm):
    VACCINATION_CHOICES = [
        (0,'0'),
        (1,'1'),
        (2,'2'),
    ]
    covid_vaccine_shots = forms.ChoiceField(
        choices=VACCINATION_CHOICES,
        required=True,
    )
    vaccine_received = forms.ChoiceField(
        choices=COVID_VACCINE_CHOICES,
        required=True,
    )
    class Meta:
        model = Asylee
        fields = ['covid_vaccine_shots','vaccine_received','sick_covid','sick_other',]

class AsyleeVaccineForm(forms.ModelForm):
    VACCINATION_CHOICES = [
        (0,'0'),
        (1,'1'),
        (2,'2'),
    ]
    covid_vaccine_shots = forms.ChoiceField(
        choices=VACCINATION_CHOICES,
        required=True,
    )
    vaccine_received = forms.ChoiceField(
        choices=COVID_VACCINE_CHOICES,
        required=True,
    )
    class Meta:
        model = Asylee
        fields = ['covid_vaccine_shots','vaccine_received',]

class AsyleeSickForm(forms.ModelForm):
    class Meta:
        model = Asylee
        fields = ['sick_covid','sick_other',]
