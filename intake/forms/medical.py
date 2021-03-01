from django import forms
from intake.models import Capacity, Medical, Profile

# Create your forms here.
class MedicalForm(forms.ModelForm):
    provider = forms.ModelChoiceField(
        queryset = Profile.objects.filter(capacities__in=Capacity.objects.filter(name='Medical'))
    )
    
    class Meta:
        model = Medical
        fields = '__all__'
        exclude = ['entered_by',]
