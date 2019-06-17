from django import forms

# from intake.models import Organization

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'city', 'state', 'point_of_contact', 'deputies', 'notes']
