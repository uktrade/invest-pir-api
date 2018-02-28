from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.core.blocks import StructBlock, CharBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_svgmap.blocks import ImageMapBlock
from wagtailmarkdown.blocks import MarkdownBlock

from invest.blocks import MarkdownAccordionItemBlock, LocationAccordionItemBlock


class RegionLandingPage(Page):
    subpage_types = ['region.regionPage']

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
    # Related region are implemented as subpages
    subpage_types = ['region.regionPage']

    show_on_frontpage = models.BooleanField(default=False)
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
             )], max_num=1, min_num=0))
    ], blank=True)

    # accordion
    subsections = StreamField([
        ('content', MarkdownAccordionItemBlock()),
        ('location', LocationAccordionItemBlock())
    ])

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('show_on_frontpage'),
        ImageChooserPanel('hero_image'),
        FieldPanel('heading'),
        StreamFieldPanel('pullout'),
        StreamFieldPanel('subsections')
    ]
