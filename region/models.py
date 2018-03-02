from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from invest.blocks.markdown import MarkdownAccordionItemBlock
from invest.blocks.location import LocationAccordionItemBlock


class RegionLandingPage(Page):
    subpage_types = ['region.RegionPage']

    # page fields
    heading = models.CharField(max_length=255)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        ImageChooserPanel('hero_image'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        region_cards = RegionPage.objects \
            .live() \
            .order_by('heading')
        context['region_cards'] = region_cards
        return context


class RegionPage(Page):
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

    # accordion
    subsections = StreamField([
        ('content', MarkdownAccordionItemBlock()),
        ('location', LocationAccordionItemBlock())
    ])

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('hero_image'),
        FieldPanel('heading'),
        StreamFieldPanel('subsections')
    ]
