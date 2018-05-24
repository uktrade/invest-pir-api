import json

from django.test import SimpleTestCase
from django.urls import reverse

from rest_framework.test import APITestCase

from investment_report.markdown import custom_markdown
from investment_report.models import Market, Sector
from countries_plus.models import Country


class TestCase(SimpleTestCase):
    def test_custom_markdown_image_paths(self):
        res1 = custom_markdown('![](/media/markdownx/test.png)', local=True)
        self.assertEquals(
            res1, '<p><img alt="" src="file:///media/markdownx/test.png" /></p>'
        )

        with self.settings(AWS_S3_CUSTOM_DOMAIN='test'):
            res2 = custom_markdown('![](/media/markdownx/test.png)', local=False)
            self.assertEquals(
                res2, '<p><img alt="" src="https://test/media/markdownx/test.png" /></p>'
            )

        with self.settings(AWS_S3_CUSTOM_DOMAIN=None):
            res2 = custom_markdown('![](/media/markdownx/test.png)', local=False)
            self.assertEquals(
                res2, '<p><img alt="" src="/media/markdownx/test.png" /></p>'
            )


class PIRAPITestCase(APITestCase):
    def setUp(self):
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

    def test_create_pir_api(self):
        res = self.client.post(reverse('pir_api'), data={
            'name': 'Rollo',
            'company': 'XXX',
            'email': 'test@example.com',
            'country': 'US',
            'sector': 'tech'
        }, format='json')
        import ipdb
        ipdb.set_trace()


        pass
