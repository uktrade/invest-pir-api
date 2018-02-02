from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.core.blocks import StructBlock, CharBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmarkdown.blocks import MarkdownBlock

from .blocks import MarkdownAccordionItemBlock


class IndustriesLandingPage(Page):
    subpage_types = ['industry.IndustryPage']

    # page fields
    heading = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
    ]


class IndustryPage(Page):
    # Related industries are implemented as subpages
    subpage_types = ['industry.IndustryPage']

    description = models.TextField()  # appears in card on external pages

    # page fields
    heading = models.CharField(max_length=255)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    pullout = StreamField([
        ('content', StructBlock([
            ('text', MarkdownBlock()),
            ('stat', CharBlock()),
            ('stat_text', CharBlock()
             )], max_num=1, min_num=1))
    ])

    # accordion
    subsections = StreamField([
        ('markdown', MarkdownAccordionItemBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('hero_image'),
        FieldPanel('heading'),
        StreamFieldPanel('pullout'),
        StreamFieldPanel('subsections')
    ]
