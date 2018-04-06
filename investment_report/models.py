from bs4 import BeautifulSoup

from sorl.thumbnail import ImageField

from django.db import models
from django.utils.html import format_html


from wagtail.core.fields import StreamField
from wagtailmarkdown.blocks import MarkdownBlock
from wagtail.admin.edit_handlers import StreamFieldPanel

from investment_report.utils import markdown_fragment


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
    content = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        frag = self.to_html_fragment()
        return format_html(frag)

    def to_html_fragment(self):
        return markdown_fragment(self.content)


# Begin spam of table models.

class SectorOverview(PDFSection):
    SECTION = 1
    NAME = '1 - Sector Overview'
    sector = models.ForeignKey(Sector, unique=True)


class KillerFacts(PDFSection):
    SECTION = 2
    NAME = '2 - Killer Facts'
    sector = models.ForeignKey(Sector, unique=True)


class MacroContextBetweenCountries(PDFSection):
    SECTION = 3
    NAME = '3 - Macro Context'
    market = models.ForeignKey(Market, unique=True)


class UKMarketOverview(PDFSection):
    SECTION = 4
    SINGLETON = True
    NAME = '4 - UK Market Overview'


class UKBusinessInfo(PDFSection):
    SECTION = 5
    SINGLETON = True
    NAME = '5 - Business Overview'


class UKGeographicOverview(PDFSection):
    SECTION = 6
    SINGLETON = True
    NAME = '6 - Business Overview'


class TalentAndEducationGeneric(PDFSection):
    SECTION = 7
    SINGLETON = True
    NAME = '7.1 - Talent & Education (Generic)'


class TalentAndEducationBySector(PDFSection):
    SECTION = 7
    sector = models.ForeignKey(Sector, unique=True)
    NAME = '7.2 - Talent & Education (Sector)'


class SectorInitiatives(PDFSection):
    SECTION = 8
    sector = models.ForeignKey(Sector, unique=True)
    NAME = '8 - Sector Initiatives'


class RDandInnovation(PDFSection):
    SECTION = 9
    NAME = '9 - R&D and Innovation'
    sector = models.ForeignKey(Sector, unique=True)


class RDandInnovationCaseStudy(PDFSection):
    SECTION = 10
    market = models.ForeignKey(Sector, unique=True)
    NAME = '10 - Case Study'


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
    NAME = '13 - Services Offered'


class CallToAction(PDFSection):
    SECTION = 14
    SINGLETON = True
    NAME = '14 - Call to action'


class Testimonials(PDFSection):
    SECTION = 15
    SINGLETON = True
    NAME = '15 - Testimonials'
