from django import forms
from intake.choices import DETENTION_TYPE_CHOICES
from intake.forms.forms import DateInput
from intake.models import HeadOfHousehold, IntakeBus, Language

# Create your forms here.
class HeadOfHouseholdForm(forms.ModelForm):
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
    languages = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset = Language.objects.all(),
        required=True,
        label='Languages spoken'
    )
    detention_type = forms.ChoiceField(
        choices=DETENTION_TYPE_CHOICES,
        required=True,
    )
    is_currently_sick = forms.BooleanField(
        # help_text='Is sick now'
        required=False
    )
    shirt_size = forms.CharField(
        help_text="E.g. infant, 2T, children's large, medium, extra large",
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
            'detention_type',
            'days_traveling',
            'days_detained',
            'country_of_origin',
            'had_covid_disease',
            'had_covid_vaccine',
            'is_currently_sick',
            'needs_medical_attention',
            'shirt_size',
            'pant_size',
            'shoe_size',
            'underwear_size',
            'notes',
        ]
