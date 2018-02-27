from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.blocks import CharBlock, StructBlock
from wagtail.core.fields import StreamField

from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
    heading = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=255)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    how_we_help = StreamField(
        [
            (
                'items',
                StructBlock([
                    ('icon', ImageChooserBlock()),
                    ('text', CharBlock()),
                ])
            )
        ],
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('sub_heading'),
        ImageChooserPanel('hero_image'),
        StreamFieldPanel('how_we_help')
    ]

    def get_context(self, request):
        # imports here, as otherwise a circular dependency can happen
        # during the initial migration
        from sector.models import SectorPage
        from setup_guide.models import SetupGuidePage
        context = super().get_context(request)
        sector_cards = SectorPage.objects \
            .live() \
            .filter(show_on_frontpage=True) \
            .order_by('heading')
        setup_guide_cards = SetupGuidePage.objects \
            .live() \
            .order_by('heading')
        context.update(
            sector_cards=sector_cards,
            setup_guide_cards=setup_guide_cards,
        )
        return context
