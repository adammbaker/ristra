from django import forms
from intake.models import Organization

# from intake.models import Organization

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'city', 'state', 'url', 'associated_airport', 'notes']

#
# class OrganizationValidateForm(forms.ModelForm):
#     token = forms.CharField(
#         max_length=6,
#         help_text='Please enter your 6-digit token here'
#     )
#
#     class Meta:
#         model = Organization
#         fields = ['token',]
