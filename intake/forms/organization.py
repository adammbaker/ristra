from django import forms
from intake.models import Organization

# from intake.models import Organization

class OrganizationForm(forms.ModelForm):
    url = forms.CharField(
        required=False
    )

    class Meta:
        model = Organization
        fields = ['name', 'city', 'state', 'url', 'airport_of_record', 'notes']

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
