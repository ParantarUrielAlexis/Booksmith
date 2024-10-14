# account/forms.py

from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'birthdate', 'bio']  # Add bio if it's in your Profile model

    # Add custom validation if needed
    def clean(self):
        cleaned_data = super().clean()
        # Perform additional validation if needed
        return cleaned_data
