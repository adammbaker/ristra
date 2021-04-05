from django import forms
from intake.choices import COVID_VACCINE_CHOICES
from intake.forms.forms import DateInput
from intake.models import Asylee

# Create your forms here.
class AsyleeForm(forms.ModelForm):
    # a_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={'placeholder': 'A-'},
    #     )
    # )
    phone_number = forms.CharField(
        required=False
    )
    date_of_birth = forms.DateField(
        help_text="MM/DD/YYYY",
        widget=DateInput(
            attrs={
                'min':'1900-01-01',
                'max':'2100-12-31',
                'pattern':'[0-9]{4}-[0-9]{2}-[0-9]{2}',
            }
        ),
    )
    is_currently_sick = forms.BooleanField(
        # help_text='Is sick now'
        required=False
    )
    class Meta:
        model = Asylee
        fields = ['name','a_number','sex','date_of_birth','phone_number','had_covid_disease','had_covid_vaccine', 'is_currently_sick', 'needs_medical_attention','notes',]

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
        fields = ['vaccine_received','covid_vaccine_doses','sick_covid','sick_other',]

class AsyleeVaccineForm(forms.ModelForm):
    VACCINATION_CHOICES = [
        (0,'0'),
        (1,'1'),
        (2,'2'),
    ]
    covid_vaccine_doses = forms.ChoiceField(
        choices=VACCINATION_CHOICES,
        required=True,
    )
    vaccine_received = forms.ChoiceField(
        choices=COVID_VACCINE_CHOICES,
        required=True,
    )
    class Meta:
        model = Asylee
        fields = ['vaccine_received','covid_vaccine_doses',]

class AsyleeSickForm(forms.ModelForm):
    class Meta:
        model = Asylee
        fields = ['sick_covid','sick_other',]
