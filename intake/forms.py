from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from intake.models import VolunteerTypes

class SignUpForm(UserCreationForm):
    name = forms.CharField(help_text="First and last name", max_length=300)
    email = forms.EmailField(max_length=300, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(help_text="Phone number", max_length=300)
    volunteer_type = forms.ModelMultipleChoiceField(queryset=VolunteerTypes.objects.all())

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phone_number', 'volunteer_type', 'password1', 'password2',)
