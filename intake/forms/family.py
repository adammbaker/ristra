from django import forms
from intake.choices import LANGUAGE_CHOICES
from intake.forms.forms import DateInput
from intake.models import HeadOfHousehold, IntakeBus, Language

# Create your forms here.
class FamilyForm(forms.ModelForm):
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

    # def __init__(self, *args, **kwargs):
    #     vol_avails = kwargs.pop('vol_avail')
    #     super(self.__class__, self).__init__(*args, **kwargs)
    #     self.fields['intake_by'].queryset = vol_avails

    class Meta:
        model = HeadOfHousehold
        fields = ['name','sex','date_of_birth','phone_number','tsa_done','legal_done','languages','lodging','destination_city','state','days_traveling','days_detained','country_of_origin','notes',]
