from django import forms

from intake.models import Families

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Families
        exclude = ['id']
