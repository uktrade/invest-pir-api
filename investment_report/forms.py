from django import forms
from django_countries.fields import CountryField
from investment_report.models import Market, Sector


class PIRForm(forms.Form):
    market = CountryField().formfield(required=True)
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.all(), required=True,
    )
    name = forms.CharField(required=True)
    company = forms.CharField(required=True)
    email = forms.EmailField(required=True)
