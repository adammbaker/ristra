from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from intake.choices import CAPACITY_CHOICES, LANGUAGE_CHOICES
from intake.models import Capacity, Language, Lead, Organization, Profile, SiteCoordinator

# class TeamLeadSignUpForm(UserCreationForm):
#     # languages = forms.MultipleChoiceField(
#     #     help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#     #     choices=LANGUAGE_CHOICES,
#     #     required=True
#     # )
#     # capacities = forms.MultipleChoiceField(
#     #     help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#     #     choices=CAPACITY_CHOICES,
#     #     required=True
#     # )
#     languages = forms.ModelMultipleChoiceField(
#         help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#         queryset = Language.objects.all(),
#         required=True
#     )
#     capacities = forms.ModelMultipleChoiceField(
#         help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#         queryset = Capacity.objects.all(),
#         required=True
#     )
#     specialty = forms.ChoiceField(
#         choices=CAPACITY_CHOICES,
#         widget=forms.Select,
#         required=True,
#         help_text='Your area of specialty as team lead'
#     )
#     organization = forms.ModelChoiceField(
#         queryset=Lead.organization.get_queryset(id__gt=0),
#         widget=forms.Select,
#         required=True,
#         help_text='The organization for which you are a team lead'
#     )

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'name', 'email', 'organization', 'phone_number', 'languages', 'capacities', 'specialty', 'password1', 'password2',)

#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_team_lead = True
#         user.save()
#         lead = Lead.objects.create(user=user)
#         lead.specialty = self.cleaned_data.get('specialty')
#         lead.save()
#         return user

# class SiteCoordinatorSignUpForm(UserCreationForm):
#     # languages = forms.MultipleChoiceField(
#     #     help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#     #     choices=LANGUAGE_CHOICES,
#     #     required=True
#     # )
#     # capacities = forms.MultipleChoiceField(
#     #     help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#     #     choices=CAPACITY_CHOICES,
#     #     required=True
#     # )
#     languages = forms.ModelMultipleChoiceField(
#         help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#         queryset = Language.objects.all(),
#         required=True
#     )
#     capacities = forms.ModelMultipleChoiceField(
#         help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#         queryset = Capacity.objects.all(),
#         required=True
#     )

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'name', 'email', 'phone_number', 'languages', 'capacities', 'password1', 'password2',)

#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         # do not set is_site_coordinator to True until Org is validated
#         user.is_site_coordinator = True
#         user.save()
#         poc = SiteCoordinator.objects.create(user=user)
#         # poc.specialty = self.cleaned_data.get('specialty')
#         return user

# class VolunteerSignUpForm(UserCreationForm):
#     # languages = forms.MultipleChoiceField(
#     #     help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#     #     choices=LANGUAGE_CHOICES,
#     #     required=True
#     # )
#     # capacities = forms.MultipleChoiceField(
#     #     help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#     #     choices=CAPACITY_CHOICES,
#     #     required=True
#     # )
#     languages = forms.ModelMultipleChoiceField(
#         help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#         queryset = Language.objects.all(),
#         required=True
#     )
#     capacities = forms.ModelMultipleChoiceField(
#         help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
#         queryset = Capacity.objects.all(),
#         required=True
#     )
#     phone_number = forms.CharField(
#         help_text='Your phone number will be kept private and used only if necessary to contact you.'
#     )

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username', 'name', 'email', 'phone_number', 'languages', 'capacities', 'password1', 'password2',)
#         # fields = ('username', 'name', 'email', 'phone_number', 'languages', 'capacities', 'password1', 'password2',)


# Sign Up Form
class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(
    #     max_length=30,
    #     required=False,
    #     help_text='Optional'
    # )
    # last_name = forms.CharField(
    #     max_length=30,
    #     required=False,
    #     help_text='Optional'
    # )
    email = forms.EmailField(
        max_length=254,
        help_text='Enter a valid email address'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
            # 'first_name',
            # 'last_name',

class ProfileForm(forms.ModelForm):
    ROLE_CHOICES=[
        ('volunteer', 'Volunteer'),
        ('team_lead','Team Lead'),
        ('site_coordinator','Site Coordinator'),
    ]
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
    phone_number = forms.CharField(
        help_text='Your phone number will be kept private and used only if necessary to contact you.'
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Profile
        fields = (
            'name',
            'languages',
            'capacities',
            'phone_number',
            'role',
        )
