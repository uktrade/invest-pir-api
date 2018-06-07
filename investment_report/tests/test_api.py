import boto3

from io import BytesIO
from unittest.mock import patch

from django.urls import reverse, resolve
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

        sector = Sector.objects.create(
            name='tech',
            display_name='tech',
        )

        market.countries=[country]
        market.save()

        self.mock_ses = mock_ses()
        self.mock_s3 = mock_ses()

        self.mock_s3.start()
        self.mock_ses.start()

        self.patcher = patch('investment_report.models.investment_report_pdf_generator')
        self.mock_generator = self.patcher.start()
        self.mock_generator.return_value = BytesIO(DATA)
        self.conn = boto3.resource('s3', region_name=settings.AWS_DEFAULT_REGION)
        self.conn.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)


    def tearDown(self):
        self.mock_generator.stop()
        self.mock_s3.stop()
        self.mock_ses.stop()

    def test_create_pir_api(self):
        res = self.client.post(reverse('pir_api'), data={
            'name': 'Rollo',
            'company': 'XXX',
            'email': 'test@example.com',
            'country': 'US',
            'sector': 'tech'
        }, format='json')

        self.assertEquals(res.status_code, 201)

        id_ = res.json()['id']

        res = self.client.get(
            reverse('pir_api_detail', args=[id_])
        )

        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.json()['pdf'])

        report = PIRRequest.objects.get(id=id_)

        body = self.conn.Object(
            settings.AWS_STORAGE_BUCKET_NAME,
            'media/{}'.format(report.pdf.name)
        ).get()['Body'].read()

        # Assert creation of s3 object
        self.assertEquals(body, DATA)
