from django import forms

from intake.models import Families

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Families
        fields = {'family_name','taken_in_by','lodging','destination','intake_bus','sponsor','travel','travel_permission_date','notes'}
