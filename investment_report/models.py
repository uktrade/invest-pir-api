import logging
import datetime
import uuid

from collections import OrderedDict

from sorl.thumbnail import ImageField
from django.utils import timezone

from django.db import models
from django.utils import translation

from countries_plus.models import Country
from markdownx.models import MarkdownxField
from django.core.files import File

from notifications_python_client.errors import HTTPError


logger = logging.getLogger(__name__)


class PIRRequest(models.Model):
    country = models.ForeignKey(Country, null=True)
    market = models.ForeignKey('Market')
    sector = models.ForeignKey('Sector')
    name = models.CharField(max_length=255)
    lang = models.CharField(max_length=255, default='en')
    company = models.CharField(max_length=255)
    email = models.EmailField()
    date_created = models.DateField(default=timezone.now)
    pdf = models.FileField()

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


class MarketLogo(models.Model):
    name = models.CharField(max_length=255)
    image = ImageField()
    market = models.ForeignKey(Market)

    def __str__(self):
        return self.name


class SectorLogo(models.Model):
    name = models.CharField(max_length=255)
    image = ImageField()
    sector = models.ForeignKey(Sector)

    def __str__(self):
        return self.name


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


class SectorOverview(PDFSection):
    SECTION = 1
    TRANSLATION_FIELDS = (
        PDFSection.TRANSLATION_FIELDS +
        ['footer_image_copy', 'footer_image_copy_attribution']
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
        verbose_name = verbose_name_plural = '1 - Sector Overview'


class KillerFacts(PDFSection):
    SECTION = 2
    sector = models.ForeignKey(Sector)

    class Meta:
        verbose_name = verbose_name_plural = '2 - Killer Facts'


class MacroContextBetweenCountries(PDFSection):
    SECTION = 3
    market = models.ForeignKey(Market)

    class Meta:
        verbose_name = verbose_name_plural = '3 - Macro Context'


class UKMarketOverview(PDFSection):
    SECTION = 4
    SINGLETON = True
    TRANSLATION_FIELDS = ['body_image']

    # No body
    content = None
    body_image = models.FileField(
        help_text=(
            'Fact sheet SVG overlayed on background of background. Don\'t edit '
            'unless you know what you are doing. Viewbox needs to be carefully '
            'calibrated here'))

    background_image = models.ImageField()

    class Meta:
        verbose_name = verbose_name_plural = '4 - UK Market Overview'


class UKBusinessInfo(PDFSection):
    SECTION = 5
    SINGLETON = True
    TRANSLATION_FIELDS = ['body_image']

    # No body
    content = None
    body_image = models.FileField(
        help_text=(
            'Fact sheet SVG overlayed on background of background. Don\'t edit '
            'unless you know what you are doing. Viewbox needs to be carefully '
            'calibrated here'))

    background_image = models.ImageField()

    class Meta:
        verbose_name = verbose_name_plural = '5 - Business Info'


class UKGeographicOverview(PDFSection):
    SECTION = 6
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '6 - Geographic Overview'


class TalentAndEducationBySector(PDFSection):
    SECTION = 7
    sector = models.ForeignKey(Sector)

    class Meta:
        verbose_name = verbose_name_plural = '7.2 - Talent & Education (Sector)'


class SectorInitiatives(PDFSection):
    SECTION = 8
    sector = models.ForeignKey(Sector)

    class Meta:
        verbose_name = verbose_name_plural = '8 - Sector Initiatives'


class RDandInnovation(PDFSection):
    SECTION = 9
    sector = models.ForeignKey(Sector)

    class Meta:
        verbose_name = verbose_name_plural = '9 - R&D and Innovation'


class NetworkAndSupport(PDFSection):
    SECTION = 10
    background_image = models.ImageField()
    sector = models.ForeignKey(Sector)

    class Meta:
        verbose_name = verbose_name_plural = '11 - Network And Support'


class RDandInnovationCaseStudy(PDFSection):
    SECTION = 11.1
    sector = models.ForeignKey(Sector)

    class Meta:
        verbose_name = verbose_name_plural = '10 - Case Study'


class VideoCaseStudy(PDFSection):
    """
    Todo:
    """
    SECTION = 11.2
    sector = models.ForeignKey(Sector)

    class Meta:
        verbose_name = verbose_name_plural = '10.1 Video case study'


class WhoIsHere(PDFSection):
    SECTION = 12
    TRANSLATION_FIELDS = []
    background_image = models.ImageField()

    # No body
    content = None

    class Meta:
        verbose_name = verbose_name_plural = '12 - Who\'s here (background image)'


class ServicesOfferedByDIT(PDFSection):
    SECTION = 13
    SINGLETON = True
    footer_image = models.ImageField(
        help_text='Image at bottom of this page'
    )

    class Meta:
        verbose_name = verbose_name_plural = '13 - Services Offered'


class CallToAction(PDFSection):
    SECTION = 15
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '14 - Call to action'


class Contact(PDFSection):
    SECTION = 15
    SINGLETON = True

    TRANSLATION_FIELDS = (
        PDFSection.TRANSLATION_FIELDS +
        ['title', ]
    )

    title = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    background_image = models.ImageField()

    class Meta:
        verbose_name = verbose_name_plural = '15 - Contact'


class LastPage(PDFSection):
    SECTION = 16
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '16 - Last Page'


sections = sorted(PDFSection.__subclasses__(), key=lambda x: x.SECTION)

page_registry = OrderedDict({
    m.__name__: m for m in sections
})
