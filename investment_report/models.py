from bs4 import BeautifulSoup

from django.db import models
from django.utils.html import format_html

from wagtail.core.fields import StreamField
from wagtailmarkdown.blocks import MarkdownBlock
from wagtail.admin.edit_handlers import StreamFieldPanel

from investment_report.utils import markdown_fragment

# Create your models here.
class Sector(models.Model):
    pass


class Market(models.Model):
    pass


class PDFSection(models.Model):
    class Meta:
        abstract = True


class FrontPage(PDFSection):
    content = models.TextField()

    def to_html_fragment(self):
        return markdown_fragment(self.content)

    def __str__(self):
        frag = self.to_html_fragment()
        return format_html(frag)
