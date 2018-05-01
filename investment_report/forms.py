from django import forms
from django_countries.fields import CountryField
from investment_report.models import Market, Sector


class PIRForm(forms.Form):
    market = CountryField().formfield(required=True)
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.all(), required=True,
    )
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    company = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': ''})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': ''})
    )

    def clean_market(self):
        data = self.cleaned_data['market']

        market = Market.objects.filter(countries__iso=data).first()

        if not market:
            raise forms.ValidationError("No market found for country.")

        return market
