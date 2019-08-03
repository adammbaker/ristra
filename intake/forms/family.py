from django import forms
from intake.choices import LANGUAGE_CHOICES
from intake.models import Family, Language

# Create your forms here.
class FamilyForm(forms.ModelForm):
    # languages = forms.MultipleChoiceField(
    #     help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
    #     choices=LANGUAGE_CHOICES,
    #     required=True,
    #     label='Languages spoken'
    # )
    languages = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset = Language.objects.all(),
        required=True,
        label='Languages spoken'
    )

    class Meta:
        model = Family
        fields = ['family_name','languages','intake_by','lodging','destination_city','state','days_traveling','days_detained','country_of_origin','notes',]
