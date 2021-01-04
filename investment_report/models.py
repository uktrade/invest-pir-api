import logging
import datetime
import uuid

from collections import OrderedDict

from django.utils import timezone

from django.db import models
from django.utils import translation

from countries_plus.models import Country
from markdownx.models import MarkdownxField
from django.core.files import File

from notifications_python_client.errors import HTTPError
from config.s3 import PDFS3Boto3Storage


logger = logging.getLogger(__name__)


class PIRRequest(models.Model):
    country = models.ForeignKey(Country, null=True)
    market = models.ForeignKey('Market')
    sector = models.ForeignKey('Sector')
    name = models.CharField(max_length=255)
    lang = models.CharField(max_length=255, default='en')
    company = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255, null=True)
    date_created = models.DateField(default=timezone.now)
    gdpr_optin = models.BooleanField(default=False)

    # Specify other bucket
    pdf = models.FileField(storage=PDFS3Boto3Storage())

    def create_pdf(self, notify=True):
        from investment_report.utils import (
            investment_report_pdf_generator, send_investment_email
        )

        with translation.override(self.lang):
            pdf_hash = (
                '{}-{}-{}-{}.pdf'.format(
                    self.company, self.lang, datetime.date.today().isoformat(),
                    str(uuid.uuid4()).split('-')[0]
                )
            )

            pdf_file = investment_report_pdf_generator(
                self.market, self.sector, self.company
            )

            self.pdf.save(pdf_hash, File(pdf_file))
            self.save()

            pdf_file.close()

            if notify:
                try:
                    send_investment_email(self)
                except HTTPError as e:
                    logger.error('Failed to send email {}'.format(e.message))


class Sector(models.Model):
    TRANSLATION_FIELDS = ['display_name']
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.display_name


class Market(models.Model):
    name = models.CharField(max_length=255)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.name


class MarketContact(models.Model):
    """
    Contact details for the contact box. Can be configured by market.
    A version without any market designation is used as the default template for all
    contact details. Any market can onverride one or all of the fields to display their
    own variants
    """
    TRANSLATION_FIELDS = []
    market = models.ForeignKey(Market, null=True, blank=True)
    first_title = models.CharField(max_length=250, null=True, blank=True, help_text=(
        'Title appearing only on the first contact box'
    ))
    title = models.CharField(max_length=250, null=True, blank=True, help_text=(
        'Title appearing in any other contact box besides the first'
    ))
    text = models.CharField(max_length=500, null=True, blank=True)
    contact_display_link = models.CharField(max_length=250, null=True, blank=True, help_text=(
        'The contact url display'
    ))
    contact_url = models.CharField(max_length=500, null=True, blank=True, help_text=(
        'The actual contact page url'
    ))
    email_address = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return 'Contact {}'.format(self.market)


class PDFSection(models.Model):
    SINGLETON = False
    SECTION = 999
    TRANSLATION_FIELDS = ['content']

    content = MarkdownxField(
        help_text=(
            'Markdown input. Please refer to '
            'https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet '
            'for intructions. Images may be dragged and droped into the editor'
        )
    )
    header_color = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        help_text="Overide default header text colour (for dark backgrounds)"
    )

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, 'sector'):
            return 'Sector: {}'.format(self.sector.name.title())

        if hasattr(self, 'market'):
            return 'Market: {}'.format(self.market.name.title())

        return 'Generic'


# Begin spam of table models.
class FrontPage(PDFSection):
    SECTION = 0
    SINGLETON = False
    TRANSLATION_FIELDS = []

    def __str__(self):
        return 'Front page - {}'.format(self.sector)

    # No body
    content = None
    background_image = models.FileField()
    sector = models.ForeignKey(Sector)

    class Meta:
        verbose_name = verbose_name_plural = '0 - Front Page'


class ContentsPage(PDFSection):
    SECTION = 0
    SINGLETON = False
    TRANSLATION_FIELDS = []

    def __str__(self):
        return 'Table of Contents - {}'.format(self.sector)

    # No body
    content = None
    background_image = models.FileField()
    sector = models.ForeignKey(Sector)

    class Meta:
        verbose_name = verbose_name_plural = '0 - Table of Contents'


class SectorOverview(PDFSection):
    SECTION = 1
    TRANSLATION_FIELDS = (
        PDFSection.TRANSLATION_FIELDS + ['footer_image_copy', 'footer_image_copy_attribution']
    )

    sector = models.ForeignKey(Sector)
    footer_image = models.ImageField(
        help_text='Image at bottom of this page'
    )
    footer_image_copy = models.TextField(
        blank=True,
        help_text='Text overlayed on image'
    )
    footer_image_copy_attribution = models.TextField(
        blank=True,
        help_text='Smaller text overlayed on image'
    )

    class Meta:
        verbose_name = verbose_name_plural = '1 - A Great Home for Company'


class KillerFacts(PDFSection):
    SECTION = 2
    sector = models.ForeignKey(Sector)
    background_image = models.ImageField(
        help_text='Background image for this page',
        null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = '2 - Achieving Great Things in Sector'


class MacroContextBetweenCountries(PDFSection):
    SECTION = 3
    market = models.ForeignKey(Market)
    background_image = models.ImageField(
        help_text='Background image for this page',
        null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = '3 - Links that are already strong'


class UKMarketOverview(PDFSection):
    SECTION = 4
    SINGLETON = True
    TRANSLATION_FIELDS = ['body_image']

    # No body
    content = None
    body_image = models.FileField(
        help_text=(
            'Fact sheet SVG overlayed on background of background. '
            'Don\'t edit unless you know what you are doing. '
            'Viewbox needs to be carefully calibrated here'))

    background_image = models.ImageField()

    class Meta:
        verbose_name = verbose_name_plural = '4 - UK Market Overview'


class SmartWorkforceSector(PDFSection):
    SECTION = 5
    MULTI_PAGE = True
    sector = models.ForeignKey(Sector)
    sub_page = models.SmallIntegerField(
        default=0,
        help_text="For multiple sub-pages of this page, number them here. ")
    background_image = models.ImageField(
        help_text='Background image for the left panel',
        null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = '5. Smart Workforce'

    def __str__(self):
        return 'Smart Workforce: {} [{}]'.format(self.sector, self.sub_page)


class CaseStudySector(PDFSection):
    SECTION = 7
    MULTI_PAGE = True
    sector = models.ForeignKey(Sector)
    sub_page = models.SmallIntegerField(
        default=0,
        help_text="For multiple sub-pages of this page, number them here. ")
    company_name = models.CharField(max_length=250, null=True, blank=True)
    background_image = models.ImageField(
        help_text='Background image for the left panel',
        null=True, blank=True
    )
    logo_image = models.ImageField(
        help_text='Company Logo image',
        null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = '7. Case Study'

    def __str__(self):
        return 'Case Study: {} {} [{}]'.format(self.sector, self.company_name, self.sub_page)


class SectorInitiatives(PDFSection):
    SECTION = 6
    sector = models.ForeignKey(Sector)
    background_image = models.ImageField(
        help_text='Background image for this page',
        null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = '6 - Sector in the UK'


class HowWeCanHelp(PDFSection):
    SECTION = 8
    SINGLETON = True

    background_image = models.ImageField(
        help_text='Background image for the right hand side',
        null=True, blank=True
    )

    class Meta:
        verbose_name = verbose_name_plural = '8 - How we can help'


class LastPage(PDFSection):
    SECTION = 9
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '9 - Last Page'


sections = sorted(PDFSection.__subclasses__(), key=lambda x: x.SECTION)

page_registry = OrderedDict({
    m.__name__: m for m in sections
})
