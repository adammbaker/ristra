from django import forms

from intake.models import Organizations

class OrganizationForm(forms.ModelForm):
    name = forms.CharField(label="Name of the organization", help_text="Name of the organization", required=True)
    head_name = forms.CharField(label="Name of the head of the organization", help_text="Name of the organization", required=True)
    head_email = forms.EmailField(label="Email of organization head", help_text="Email of the organization head", required=True)
    head_phone_number = forms.CharField(label="Phone number of organization head", help_text="Phone number of the organization head", required=True)

    class Meta:
        model = Organizations
        fields = ['name', 'location', 'head_name','head_email','head_phone_number']
