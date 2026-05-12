from django import forms
from .models import Flight, Site


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['site', 'aws_url', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'site': forms.Select(),
            'aws_url': forms.TextInput(attrs={'placeholder': 'https://...'}),
        }
        labels = {
            'site': 'Site',
            'aws_url': 'AWS URL',
            'date': 'Flight Date',
        }
