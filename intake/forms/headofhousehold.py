from django import forms
from intake.choices import LANGUAGE_CHOICES
from intake.forms.forms import DateInput
from intake.models import HeadOfHousehold, IntakeBus, Language

# Create your forms here.
class HeadOfHouseholdForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False
    )
    date_of_birth = forms.DateField(
        help_text="MM/DD/YYYY",
        widget=DateInput(),
    )
    languages = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset = Language.objects.all(),
        required=True,
        label='Languages spoken'
    )
    is_currently_sick = forms.BooleanField(
        # help_text='Is sick now'
        required=False
    )

    # def __init__(self, *args, **kwargs):
    #     vol_avails = kwargs.pop('vol_avail')
    #     super(self.__class__, self).__init__(*args, **kwargs)
    #     self.fields['intake_by'].queryset = vol_avails

    class Meta:
        model = HeadOfHousehold
        fields = [
            'name',
            'sex',
            'a_number',
            'date_of_birth',
            'phone_number',
            'languages',
            'lodging',
            'destination_city',
            'state',
            'days_traveling',
            'days_detained',
            'country_of_origin',
            'had_covid_disease',
            'had_covid_vaccine',
            'is_currently_sick',
            'notes',
        ]
