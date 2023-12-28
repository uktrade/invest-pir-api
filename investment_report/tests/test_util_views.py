from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from countries_plus.models import Country

from investment_report.models import Market, Sector, PIRRequest


class UtilsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', email='admin@example.com',
            is_superuser=True, is_staff=True,
            password='top_secret')
        self.user.set_password('test')
        self.user.save()
        self.client.login(username='admin', password='test')

        self.market = Market.objects.create(name='china')
        self.sector = Sector.objects.create(
            name='tech',
            display_name='Technology'
        )

    def test_html_view(self):
        response = self.client.get(
            reverse('investment_report_html', args=[
                'en', 'china', 'tech'
            ])
        )
        self.assertEquals(response.context['sector'], 'Technology')
        self.assertEquals(response['content-language'], 'en')

        response = self.client.get(
            reverse('investment_report_html', args=[
                'es', 'china', 'tech'
            ])
        )

        # Actual language code won't be changed
        self.assertEquals(response.context['lang'], 'es')

    def test_pdf_view(self):
        response = self.client.get(
            reverse('investment_report_pdf', args=[
                'en', 'china', 'tech'
            ])
        )

        self.assertEquals(response.context['sector'], 'Technology')
        self.assertEquals(response['content-type'], 'application/pdf')

    def test_pir_csv_view(self):
        # Clean up the db - if test ran after test_api
        PIRRequest.objects.all().delete()

        country = Country.objects.create(
            iso='US', iso3='USA', iso_numeric='1', name='USA'
        )

        PIRRequest.objects.create(
            country=country,
            sector=self.sector,
            market=self.market,
            name='test1',
            company='testco1',
            email='test1@example.com'
        )

        response = self.client.get(reverse('pir_csv'))
        self.assertEquals(len(response.content.split()), 2)

        PIRRequest.objects.create(
            country=country,
            sector=self.sector,
            market=self.market,
            name='test1',
            company='testco1',
            email='test1@example.com'
        )

        response = self.client.get(reverse('pir_csv'))
        self.assertEquals(len(response.content.split()), 3)

        # Extract the header into a set
        header_set = set(response.content.decode('utf').split()[0].split(','))

        expected_headers = set([
            'id', 'country', 'market__name', 'sector__name', 'name',
            'lang', 'company', 'email', 'phone_number', 'date_created',
            'gdpr_optin'
        ])

        self.assertEquals(header_set, expected_headers)
