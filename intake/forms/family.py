from django import forms
from intake.models import Family

# Create your forms here.
class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['family_name','languages','intake_by','lodging','destination_city','state','days_traveling','days_detained','country_of_origin','notes',]
