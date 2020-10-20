from PyPDF2 import PdfFileReader

from django.test import TestCase, RequestFactory
from django.utils import translation
from django.urls import reverse
from django.contrib.auth import get_user_model

from investment_report.views.utils import pir_csv

# Importing this one as this is a simple model without sector
# or market
from investment_report.models import (
    Sector, Market, FrontPage, SectorOverview, KillerFacts,
    MacroContextBetweenCountries, UKMarketOverview, UKBusinessInfo,
    UKGeographicOverview, TalentAndEducationBySector, NetworkAndSupport,
    SectorInitiatives, RDandInnovation,
    ServicesOfferedByDIT, Contact, LastPage,
)  # RDandInnovationCaseStudy, VideoCaseStudy,

from investment_report.utils import (
    filter_translations_and_moderation, get_investment_report_data,
    investment_report_html_generator, investment_report_pdf_generator
)

from moderation.constants import (
    MODERATION_READY_STATE, MODERATION_STATUS_APPROVED
)


class FiltersModerationTranslationTestCase(TestCase):

    def test_moderation_filtering(self):
        geographic_overview = UKGeographicOverview.objects.create(
            content_en='English',
            content_es='Spanish'
        )

        self.assertEquals(
            UKGeographicOverview.objects.count(), 0
        )

        self.assertEquals(
            UKGeographicOverview.unmoderated_objects.count(), 1
        )

        self.assertIsNotNone(
            filter_translations_and_moderation(UKGeographicOverview,
                                               moderated=False)
        )

        # Test object not registered with moderation
        geographic_overview.moderated_object.delete()
        self.assertIsNotNone(
            filter_translations_and_moderation(UKGeographicOverview,
                                               moderated=False)
        )

    def test_basic_language_filtering(self):
        UKGeographicOverview.objects.create(
            content_en='English',
            content_es='Spanish'
        )

        # Test with english
        moderated = filter_translations_and_moderation(UKGeographicOverview)
        unmoderated = filter_translations_and_moderation(
            UKGeographicOverview, moderated=False
        )
        self.assertIsNone(moderated)
        self.assertIsNotNone(unmoderated)

        # Test with spanish
        with translation.override('es'):
            moderated = filter_translations_and_moderation(
                UKGeographicOverview)

            unmoderated = filter_translations_and_moderation(
                UKGeographicOverview, moderated=False
            )
            self.assertIsNone(moderated)
            self.assertIsNotNone(unmoderated)

        # Test with non-existant language
        with translation.override('pt'):
            moderated = filter_translations_and_moderation(
                UKGeographicOverview)

            unmoderated = filter_translations_and_moderation(
                UKGeographicOverview, moderated=False
            )

            self.assertIsNone(moderated)
            self.assertIsNone(unmoderated)

    def test_get_investment_report_data(self):
        market = Market.objects.create(name='test')
        sector = Sector.objects.create(name='test')

        geo_overview = UKGeographicOverview.objects.create(
            content_en='English Moderated',
        )

        geo_overview.moderated_object.changed_object.content_en = (
            'English Unmoderated'
        )

        geo_overview.moderated_object.state = MODERATION_READY_STATE
        geo_overview.moderated_object.status = MODERATION_STATUS_APPROVED
        geo_overview.moderated_object.save()

        data = get_investment_report_data(
            market, sector, company_name='TestCo', moderated=True
        )

        self.assertEquals(
            data['uk_geo_overview'].content_en,
            'English Moderated'
        )

        data = get_investment_report_data(
            market, sector, company_name='TestCo', moderated=False
        )

        self.assertEquals(
            data['uk_geo_overview'].content_en,
            'English Unmoderated'
        )

    def test_investment_report_html(self):
        market = Market.objects.create(name='test')
        sector = Sector.objects.create(name='test')
        pages = investment_report_html_generator(market, sector, 'Test')

        self.assertEquals(len(pages), 2)
        self.assertIsInstance(pages[0], str)
        self.assertIsInstance(pages[1], str)

    def test_investment_report_pdf(self):
        # TODO create example data for everything - after lunch
        market = Market.objects.create(name='test')
        sector = Sector.objects.create(name='test')

        sample_content = '# Lorem Ipsum\n\nHello'

        FrontPage.objects.create(sector=sector)
        SectorOverview.objects.create(sector=sector, content=sample_content)
        KillerFacts.objects.create(sector=sector, content=sample_content)
        MacroContextBetweenCountries.objects.create(market=market,
                                                    content=sample_content)
        UKMarketOverview.objects.create()
        # UKBusinessInfo.objects.create()
        # UKGeographicOverview.objects.create(content=sample_content)
        # TalentAndEducationBySector.objects.create(sector=sector,
        #                                           content=sample_content)
        # NetworkAndSupport.objects.create(sector=sector, content=sample_content)
        SectorInitiatives.objects.create(sector=sector, content=sample_content)
        # RDandInnovation.objects.create(sector=sector, content=sample_content)
        # RDandInnovationCaseStudy.objects.create(sector=sector,
        #                                         content=sample_content)
        # VideoCaseStudy.objects.create(sector=sector, content=sample_content)
        # ServicesOfferedByDIT.objects.create(content=sample_content)
        # Contact.objects.create(content=sample_content)
        LastPage.objects.create(content=sample_content)

        pdf_io = investment_report_pdf_generator(market, sector,
                                                 'Test', moderated=False)
        reader = PdfFileReader(pdf_io)
        # Nothing else one can really do other than visual
        # inspection of the PDF
        self.assertEquals(reader.getOutlines()[0]['/Title'], 'Contents')


class PIRCSVTestCase(TestCase):
    def test_pir_csv_logs_user_downloaded(self):

        request = RequestFactory().get(reverse('pir_csv'))

        user = get_user_model().objects.create(
            email='testemail@testing123.com',
            first_name='test',
            last_name='test',
        )

        request.user = user

        with self.assertLogs('pir-csv-download', level='INFO') as cm:
            pir_csv(request)

        self.assertEqual(
            cm.output,
            ['INFO:pir-csv-download:PIR CSV downloaded by testemail@testing123.com'])  # noqa: E501
