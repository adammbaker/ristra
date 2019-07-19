from django import forms
from intake.models import Token

class TokenForm(forms.ModelForm):
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    class Meta:
        model = Token
        fields = ('notes', )
