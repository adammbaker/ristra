from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from intake.models import Capacity, TeamLead, User


class TeamLeadSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_team_lead = True
        if commit:
            user.save()
        return user


class VolunteerSignUpForm(UserCreationForm):
    capacities = forms.ModelMultipleChoiceField(
        queryset=Capacity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    phone_number = forms.CharField(
        help_text='Your phone number will be kept private and used only as necessary to contact you.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name', 'email', 'phone_number', 'capacities', 'password1', 'password2',)
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
