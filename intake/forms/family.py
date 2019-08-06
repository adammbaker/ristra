from django import forms
from intake.choices import LANGUAGE_CHOICES
from intake.models import Family, IntakeBus, Language

# Create your forms here.
class FamilyForm(forms.ModelForm):
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
        model = Family
        fields = ['family_name','languages','lodging','destination_city','state','days_traveling','days_detained','country_of_origin','notes',]
