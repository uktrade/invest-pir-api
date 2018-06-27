import boto3

from io import BytesIO
from unittest.mock import patch

from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase

from countries_plus.models import Country

from config.celery import app as celeryapp

from investment_report.models import Market, Sector, PIRRequest

from moto import mock_s3, mock_ses

DATA = b'data...'


@mock_s3
@mock_ses
class PIRAPITestCase(APITestCase):
    def setUp(self):
        celeryapp.conf.update(CELERY_ALWAYS_EAGER=True)

        country = Country.objects.create(
            iso='US', iso3='USA', iso_numeric='1', name='USA'
        )

        market = Market.objects.create(
            name='USA',
        )

        Sector.objects.create(
            name='tech',
            display_name='tech',
        )

        market.countries = [country]
        market.save()

        self.mock_ses = mock_ses()
        self.mock_s3 = mock_s3()

        self.mock_s3.start()
        self.mock_ses.start()

        self.patcher = patch(
            'investment_report.utils.investment_report_pdf_generator'
        )

        self.mock_generator = self.patcher.start()
        self.mock_generator.return_value = BytesIO(DATA)
        self.conn = boto3.resource(
            's3',
            region_name=settings.AWS_DEFAULT_REGION
        )

    def tearDown(self):
        self.mock_generator.stop()
        self.mock_ses.stop()
        self.mock_s3.stop()
        self.patcher.stop()

    def test_create_pir_api(self):
        res = self.client.post(reverse('pir_api'), data={
            'name': 'Rollo',
            'company': 'XXX',
            'email': 'test@example.com',
            'country': 'US',
            'sector': 'tech',
            'lang': 'en'
        }, format='json')

        self.assertEquals(res.status_code, 201)

        id_ = res.json()['id']

        report = PIRRequest.objects.get(id=id_)
        self.assertIsNotNone(report)

        res = self.client.post(reverse('pir_api'), data={
            'name': 1,
            'company': 2,
            'email': 'notanemail',
            'country': 'US',
            'sector': 'tech',
            'lang': 'en'
        }, format='json')

        self.assertEquals(res.status_code, 400)

        res = self.client.options(reverse('pir_api'))
        self.assertEquals(res.status_code, 200)

        expected_options_data = {
            'country': {'choices': [{'display_name': 'USA', 'value': 'US'}]},
            'market': {'choices': [{'display_name': 'USA', 'value': 'USA'}]},
            'sector': {'choices': [{'display_name': 'tech', 'value': 'tech'}]}
        }

        post_options = res.json()['actions']['POST']

        self.assertEquals(post_options['country']['choices'],
                          expected_options_data['country']['choices'])

        self.assertEquals(post_options['market']['choices'],
                          expected_options_data['market']['choices'])

        self.assertEquals(post_options['sector']['choices'],
                          expected_options_data['sector']['choices'])
