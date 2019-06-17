from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from intake.models import Capacities, Languages

class SignUpForm(UserCreationForm):
    name = forms.CharField(help_text="First and last name", max_length=300)
    email = forms.EmailField(max_length=300)
    phone_number = forms.CharField(help_text="Phone number", max_length=300)
    # languages = forms.ModelMultipleChoiceField(queryset=Languages.objects.all())
    # capacities = forms.ModelMultipleChoiceField(queryset=Capacities.objects.all())

    class Meta:
        model = User
        # fields = ('username', 'name', 'email', 'phone_number', 'languages', 'capacities', 'password1', 'password2',)
        exclude = ('campaigns', )
