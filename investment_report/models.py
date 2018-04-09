from bs4 import BeautifulSoup
from collections import OrderedDict

from sorl.thumbnail import ImageField

from django.db import models
from django.utils.html import format_html


from wagtail.core.fields import StreamField
from wagtailmarkdown.blocks import MarkdownBlock
from wagtail.admin.edit_handlers import StreamFieldPanel

from markdownx.models import MarkdownxField


class Sector(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MarketLogo(models.Model):
    name = models.CharField(max_length=255)
    image = ImageField()

    def __str__(self):
        return self.name


class SectorLogo(models.Model):
    name = models.CharField(max_length=255)
    image = ImageField()

    def __str__(self):
        return self.name


class PDFSection(models.Model):
    SINGLETON = False
    SECTION = 999
    content = MarkdownxField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.content[:10]

    def to_html_fragment(self):
        from investment_report.utils import markdown_fragment
        return markdown_fragment(self.content)


# Begin spam of table models.

class SectorOverview(PDFSection):
    SECTION = 1
    sector = models.ForeignKey(Sector, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = '1 - Sector Overview'


class KillerFacts(PDFSection):
    SECTION = 2
    sector = models.ForeignKey(Sector, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = '2 - Killer Facts'


class MacroContextBetweenCountries(PDFSection):
    SECTION = 3
    market = models.ForeignKey(Market, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = '3 - Macro Context'


class UKMarketOverview(PDFSection):
    SECTION = 4
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '4 - UK Market Overview'


class UKBusinessInfo(PDFSection):
    SECTION = 5
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '5 - Business Overview'


class UKGeographicOverview(PDFSection):
    SECTION = 6
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '6 - Geographic Overview'


class TalentAndEducationGeneric(PDFSection):
    SECTION = 7.1
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '7.1 - Talent & Education (Generic)'


class TalentAndEducationBySector(PDFSection):
    SECTION = 7.2
    sector = models.ForeignKey(Sector, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = '7.2 - Talent & Education (Sector)'


class SectorInitiatives(PDFSection):
    SECTION = 8
    sector = models.ForeignKey(Sector, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = '8 - Sector Initiatives'


class RDandInnovation(PDFSection):
    SECTION = 9
    sector = models.ForeignKey(Sector, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = '9 - R&D and Innovation'


class RDandInnovationCaseStudy(PDFSection):
    SECTION = 10
    sector = models.ForeignKey(Sector, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = '10 - Case Study'


class WhoIsHere:
    """
    Not a model
    """
    SECTION = 11


class VideoCaseStudy:
    """
    Todo:
    """
    SECTION = 12
    sector = models.ForeignKey(Sector, unique=True)


class ServicesOfferedByDIT(PDFSection):
    SECTION = 13
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '13 - Services Offered'


class CallToAction(PDFSection):
    SECTION = 14
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '14 - Call to action'


class Testimonials(PDFSection):
    SECTION = 15
    SINGLETON = True

    class Meta:
        verbose_name = verbose_name_plural = '15 - Testimonials'


sections = sorted(PDFSection.__subclasses__(), key=lambda x: x.SECTION)

page_registry = OrderedDict({
    m.__name__: m for m in sections
})
