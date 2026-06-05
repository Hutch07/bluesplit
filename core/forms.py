from django import forms
from .models import Flight, Site, User


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


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'longitude', 'latitude']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Site name'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Longitude'}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Latitude'}),
        }
        labels = {
            'name': 'Site Name',
            'longitude': 'Longitude',
            'latitude': 'Latitude',
        }


class SiteAccessForm(forms.Form):
    site = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        label='Site',
        empty_label='— Select a site —',
    )
    allowed_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().order_by('username'),
        label='Allowed Users',
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
