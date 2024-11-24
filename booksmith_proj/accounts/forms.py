# account/forms.py

from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'birthdate', 'bio']
        widgets = {
            'birthdate': forms.DateInput(attrs={
                'type': 'date',  # HTML5 date input
                'class': 'form-control',  # Add Bootstrap or custom classes for styling
            }),

        }
        labels = {
            'birthdate': 'Date of Birth',  # Optional, human-readable label

        }

    # Add custom validation for specific fields or combinations of fields
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate:
            # Example: Ensure birthdate is not in the future
            from datetime import date
            if birthdate > date.today():
                raise forms.ValidationError("The birthdate cannot be in the future.")
        return birthdate

    def clean(self):
        cleaned_data = super().clean()
        # Additional custom validation logic here
        # For example:
        # if some_condition:
        #     self.add_error('field_name', 'Error message')
        return cleaned_data
