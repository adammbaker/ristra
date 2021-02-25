from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from datetime import datetime
from intake.models import Capacity, Language

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class TimeInput(forms.TimeInput):
    input_type = "time"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)

class SignUpForm(UserCreationForm):
    name = forms.CharField(help_text="First and last name", max_length=300)
    email = forms.EmailField(max_length=300)
    phone_number = forms.CharField(help_text="Phone number", max_length=300)
    languages = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset = Language.objects.all(),
        required=True
    )
    capacities = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset = Capacity.objects.all(),
        required=True
    )
    # languages = forms.ModelMultipleChoiceField(queryset=Languages.objects.all())
    # capacities = forms.ModelMultipleChoiceField(queryset=Capacities.objects.all())

    class Meta:
        model = User
        # fields = ('username', 'name', 'email', 'phone_number', 'languages', 'capacities', 'password1', 'password2',)
        exclude = ('campaigns', )
