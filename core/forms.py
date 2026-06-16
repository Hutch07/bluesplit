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
        fields = ['name', 'longitude', 'latitude', 'proj4']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Site name'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Longitude'}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': 'Latitude'}),
            'proj4': forms.Textarea(attrs={
                'placeholder': '+proj=lcc +lat_0=39.3333333333333 +lon_0=-77.75 +lat_1=40.9666666666667 +lat_2=39.9333333333333 +x_0=600000 +y_0=0 +ellps=GRS80 +nadgrids=us_noaa_pahpgn.tif +units=us-ft +no_defs +type=crs',
                'rows': 3,
            }),
        }
        labels = {
            'name': 'Site Name',
            'longitude': 'Longitude',
            'latitude': 'Latitude',
            'proj4': 'Proj.4 String',
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
