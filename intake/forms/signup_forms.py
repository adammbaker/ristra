from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from intake.models import Capacity, Language, Lead, Organization, PointOfContact, User

class TeamLeadSignUpForm(UserCreationForm):
    languages = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset=Language.objects.all(),
        required=True
    )
    capacities = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset=Capacity.objects.all(),
        required=True
    )
    specialty = forms.ModelChoiceField(
        queryset=Lead.specialty.get_queryset(id__gt=0),
        widget=forms.Select,
        required=True,
        help_text='Your area of specialty as team lead'
    )
    organization = forms.ModelChoiceField(
        queryset=Lead.organization.get_queryset(id__gt=0),
        widget=forms.Select,
        required=True,
        help_text='The organization for which you are a team lead'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name', 'email', 'organization', 'phone_number', 'languages', 'capacities', 'specialty', 'password1', 'password2',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_team_lead = True
        user.save()
        lead = Lead.objects.create(user=user)
        lead.specialty = self.cleaned_data.get('specialty')
        lead.save()
        return user

class PointOfContactSignUpForm(UserCreationForm):
    languages = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset=Language.objects.all(),
        required=True
    )
    capacities = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset=Capacity.objects.all(),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name', 'email', 'phone_number', 'languages', 'capacities', 'password1', 'password2',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        # do not set is_point_of_contact to True until Org is validated
        user.is_point_of_contact = True
        user.save()
        poc = PointOfContact.objects.create(user=user)
        # poc.specialty = self.cleaned_data.get('specialty')
        return user

class VolunteerSignUpForm(UserCreationForm):
    languages = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset=Language.objects.all(),
        required=True
    )
    affiliations = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset=Organization.objects.all(),
        required=True
    )
    capacities = forms.ModelMultipleChoiceField(
        help_text='Ctrl-Click to select multiple; Cmd-Click on Mac',
        queryset=Capacity.objects.all(),
        required=True
    )
    phone_number = forms.CharField(
        help_text='Your phone number will be kept private and used only as necessary to contact you.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name', 'email', 'affiliations', 'phone_number', 'languages', 'capacities', 'password1', 'password2',)
        # fields = ('username', 'name', 'email', 'phone_number', 'languages', 'capacities', 'password1', 'password2',)

    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user.save()
    #     student = Student.objects.create(user=user)
    #     student.capacities.add(*self.cleaned_data.get('capacities'))
    #     return user


# class StudentInterestsForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ('interests', )
#         widgets = {
#             'interests': forms.CheckboxSelectMultiple
#         }
