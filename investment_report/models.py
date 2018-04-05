from bs4 import BeautifulSoup

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


class PDFSection(models.Model):
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
    content = models.TextField()
    sector = models.ForeignKey(Sector, unique=True)


class KillerFacts(PDFSection):
    SECTION = 2
    content = models.TextField()
    sector = models.ForeignKey(Sector, unique=True)


class MacroContextBetweenCountries(PDFSection):
    SECTION = 3
    content = models.TextField()
    sector = models.ForeignKey(Market, unique=True)


class UKMarketOverview(PDFSection):
    SECTION = 4
    content = models.TextField()


class UKBusinessInfo(PDFSection):
    SECTION = 5
    content = models.TextField()


class UKGeographicOverview(PDFSection):
    SECTION = 6
    content = models.TextField()


class TalentAndEducationGeneric(PDFSection):
    SECTION = 7
    content = models.TextField()


class TalentAndEducationBySector(PDFSection):
    SECTION = 7
    content = models.TextField()
    sector = models.ForeignKey(Market, unique=True)


class SectorInitiatives(PDFSection):
    SECTION = 8
    content = models.TextField()
    sector = models.ForeignKey(Market, unique=True)


class RDandInnovation(PDFSection):
    SECTION = 9
    content = models.TextField()
    sector = models.ForeignKey(Market, unique=True)


class RDandInnovationCaseStudy(PDFSection):
    SECTION = 10
    content = models.TextField()
    sector = models.ForeignKey(Market, unique=True)


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
    sector = models.ForeignKey(Market, unique=True)


class ServicesOfferedByDIT(PDFSection):
    SECTION = 13
    content = models.TextField()


class CallToAction(PDFSection):
    SECTION = 14
    content = models.TextField()


class Testimonials(PDFSection):
    SECTION = 15
    content = models.TextField()
