import django_countries

from django.conf import settings
from django.utils.html import escape

from countries_plus.models import Country

from rest_framework import serializers
from investment_report.models import Market, Sector, PIRRequest


class PIRSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        queryset=Country.objects.all(),
        read_only=False,
        many=False,
        required=False,
        slug_field='iso',
        allow_null=True,
    )

    market = serializers.SlugRelatedField(
        queryset=Market.objects.all(),
        read_only=False,
        many=False,
        required=False,
        slug_field='name',
        allow_null=True,
    )

    sector = serializers.SlugRelatedField(
        queryset=Sector.objects.all(),
        read_only=False,
        many=False,
        required=True,
        slug_field='name'
    )

    lang = serializers.ChoiceField(
        choices=[l[0] for l in settings.LANGUAGES],
        default=settings.LANGUAGE_CODE
    )

    name = serializers.CharField(required=True)
    company = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    pdf = serializers.FileField(read_only=True)
    date_created = serializers.DateTimeField(read_only=True)


    def validate(self, data):
        """
        Check that the start is before the stop.
        """

        country = data.get('country')
        market = data.get('market')

        if country and market:
            raise serializers.ValidationError(
                'Country and market are exclusive'
            )

        if not (country or market):
            raise serializers.ValidationError(
                'Must provide country or market'
            )

        if country:
            market = Market.objects.get(countries=country)

        data['market'] = market

        data['name'] = escape(data['name'])
        data['company'] = escape(data['company'])

        return data

    class Meta:
        model = PIRRequest
        fields = '__all__'
